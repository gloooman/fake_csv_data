import csv
import os

from celery_app import app
from creator.models import DataSet, Column
from faker import Faker
from django.core.files import File


def save_to_csv(data, filename=None):
    path = f'media/csv/{filename}.csv'
    with open(path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


@app.task
def create_scv(instance_id):
    fake = Faker()
    Faker.seed(0)
    instance = DataSet.objects.get(id=instance_id)
    filename = f'dataset_{instance_id}'

    try:
        columns = Column.objects.filter(schema_id=instance.schema.id).order_by('order')
        headers = [column.col_name for column in columns]
        with open(f'media/csv/{filename}.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for i in range(instance.rows):
                row = [column.get_fake_data(fake) for column in columns]
                writer.writerow(row)

        with open(f'media/csv/{filename}.csv', 'r') as f:
            instance.path = File(f, name=os.path.basename(f.name))
            instance.status = DataSet.Status.READY
            instance.save()
    except Exception:
        instance.status = DataSet.Status.ERROR
        instance.save()
    finally:
        os.remove(f'media/csv/{filename}.csv')
