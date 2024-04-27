import pandas as pd
from dateutil import parser
from django.core.management import BaseCommand
from tqdm import tqdm

from Themis.models.operation import Area
from Themis.models.project import ProjectStatus, ProjectType, Customer, Project


def convert_date(key, row):
    try:
        date = row.get(key)
        if date:
            date = date.strftime('%Y-%m-%d')
        else:
            return None
    except Exception as e:
        print(e)
        date = row.get(key)

    return parser.parse(date) if date else None


class Command(BaseCommand):
    help = 'Import projects from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_path', type=str, help='The path to the Excel file.')

    def handle(self, *args, **options):
        excel_path = options['excel_path']
        data = pd.read_excel(excel_path)
        for _, row in tqdm(data.iterrows()):
            # 涉及外键 需要先创建相应实例
            area = row.get('area')
            if area:
                area, _ = Area.objects.get_or_create(name=area)
                if _:
                    print(f'created {area}')

            type = row.get('type')
            if type:
                project_type, _ = ProjectType.objects.get_or_create(type=type)
                if _:
                    print(f'created {project_type}')
            status = row.get('status')
            if status:
                project_status, _ = ProjectStatus.objects.get_or_create(status=status)
                if _:
                    print(f'created {project_status}')
            customer = row.get('customer')
            if customer:
                name = customer.split('-')[0]
                location = customer.split('-')[1]
                customer, _ = Customer.objects.get_or_create(name=name, location=location)
                if _:
                    print(f'created {customer}')

            # 创建员工 已有字段

            name = row.get('name')
            initiation_date = convert_date('initiation', row)
            completion_date_est = convert_date('completion_date_est', row)
            code = row.get('code')

            project = Project.objects.create(
                name=name,
                code=code,
                area=area,
                project_type=project_type,
                project_status=project_status,
                customer=customer,
                initiation_date=initiation_date,
                completion_date_est=completion_date_est
            )

            print(f'{project} created')
