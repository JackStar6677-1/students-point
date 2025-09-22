from datetime import time, datetime
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from studentspoint.apps.accounts.models import User
from .models import ScheduleImport, Horario
from .tasks import parse_schedule_pdf


class ScheduleImportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@duocuc.cl", password="x")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @patch("studentspoint.apps.schedules.views.parse_schedule_pdf.delay")
    def test_upload_import_creates_record(self, mock_delay):
        file = SimpleUploadedFile("horario.pdf", b"dummy", content_type="application/pdf")
        resp = self.client.post("/api/horarios/import/pdf", {"file": file})
        self.assertEqual(resp.status_code, 202)
        import_id = resp.data["import_id"]
        self.assertTrue(ScheduleImport.objects.filter(id=import_id).exists())
        mock_delay.assert_called_once()
        resp2 = self.client.get(f"/api/horarios/import/{import_id}")
        self.assertEqual(resp2.status_code, 200)

    def test_parse_task_creates_horarios(self):
        imp = ScheduleImport.objects.create(usuario=self.user, file="dummy.pdf")
        sample_text = (
            "Lunes 08:00-09:30 Matematica Sala B-101\n"
            "Martes 10:00 Programacion Sala C-202"
        )

        class DummyPage:
            def extract_text(self_inner):
                return sample_text

        with patch("studentspoint.apps.schedules.tasks.PdfReader") as mock_reader, \
            patch("studentspoint.apps.schedules.tasks.schedule_class_alerts.delay"):
            mock_reader.return_value.pages = [DummyPage()]
            parse_schedule_pdf(str(imp.id))

        self.assertEqual(Horario.objects.filter(usuario=self.user).count(), 2)
        prog = Horario.objects.get(asignatura="Programacion")
        self.assertEqual(prog.fin, time(11, 30))
        imp.refresh_from_db()
        self.assertIn("duración inferida", imp.parse_log)

    @patch("studentspoint.apps.notifications.tasks.send_class_push.apply_async")
    def test_schedule_class_alerts(self, mock_apply):
        horario = Horario.objects.create(
            usuario=self.user,
            dia_semana=datetime.now().weekday(),
            inicio=time(10, 0),
            fin=time(11, 0),
            asignatura="Test",
        )
        from studentspoint.apps.notifications.tasks import schedule_class_alerts

        schedule_class_alerts(self.user.id)
        self.assertTrue(mock_apply.called)
        args, kwargs = mock_apply.call_args
        self.assertIn("eta", kwargs)

    def test_horario_crud(self):
        resp = self.client.post(
            "/api/horarios",
            {"dia_semana": 1, "inicio": "09:00", "fin": "10:00", "asignatura": "Algoritmos"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        hid = resp.data["id"]
        resp = self.client.patch(
            f"/api/horarios/{hid}", {"sala": "101"}, format="json"
        )
        self.assertTrue(resp.data["editable"])
        resp = self.client.delete(f"/api/horarios/{hid}")
        self.assertEqual(resp.status_code, 204)
