from dateutil import parser
import pandas as pd
from django.core.management import BaseCommand
from pypinyin import lazy_pinyin

from Themis.models import Employee
from Themis.models import Department, Position
from Themis.models import OA


class Command(BaseCommand):
    help = 'Import employees from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_path', type=str, help='The path to the Excel file.')

    def handle(self, *args, **options):
        excel_path = options['excel_path']
        data = pd.read_excel(excel_path)
        for _, row in data.iterrows():
            position = None
            if not pd.notna(row['department']):
                continue
            department = row['department']
            area, exist = OA.objects.get_or_create(OA_name=row['OA'])
            if area:
                department_instance, exist = Department.objects.get_or_create(area=area, department=department)
                if pd.notna(row['title']):
                    title = row['title']
                    position_instance, exist = Position.objects.get_or_create(department=department_instance,
                                                                              title=title)
                    if position_instance:
                        position = position_instance

            salary_place = row.get('salary_place')
            work_place = row.get('work_place')
            name = row.get('name')
            print(name)
            username = "".join(lazy_pinyin(name))
            email = username + '@dihuge.com'
            graduated_from = row.get('graduated_from')
            expertise = row.get('expertise')
            degree = row.get('degree')
            employee_number = row.get('employee_number')
            status = row.get('status')
            id_number = row.get('id_number')
            gender = row.get('gender')
            if gender == '男':
                gender = 'M'
            else:
                gender = 'F'
            phone = row.get('phone')
            try:
                date_joined = row.get('date_joined').strftime('%Y-%m-%d')
            except Exception as e:
                print(e)
                date_joined = row.get('date_joined')
            date_joined = parser.parse(date_joined)
            contract_place = row.get('contract_place')
            contract_renewed_times = row.get('contract_renewed_times')
            try:
                contract_start_date = row.get('contract_start_date').strftime('%Y-%m-%d')
            except Exception as e:
                print(e)
                contract_start_date = row.get('contract_start_date')
            contract_start_date = parser.parse(contract_start_date)

            try:
                contract_end_date = row.get('contract_end_date').strftime('%Y-%m-%d')
            except Exception as e:
                print(e)
                contract_end_date = row.get('contract_end_date')
            contract_end_date = parser.parse(contract_end_date)
            insurance_place = row.get('insurance_place')
            id_address = row.get('id_address')
            bank_number = row.get('bank_number')

            employee = Employee.objects.create(
                name=name,
                last_name=name[0],
                first_name=name[1:],
                username=username,
                employee_number=employee_number,
                position=position,
                date_joined=date_joined,
                salary_place=salary_place,
                work_place=work_place,
                contract_place=contract_place,
                contract_renewed_times=contract_renewed_times,
                contract_start_date=contract_start_date,
                contract_end_date=contract_end_date,
                insurance_place=insurance_place,
                bank_number=bank_number,
                gender=gender,
                status=status,
                expertise=expertise,
                phone=phone,
                id_number=id_number,
                id_address=id_address,
                graduated_from=graduated_from,
                degree=degree,
                email=email
            )

            print(f'Imported {employee}')
