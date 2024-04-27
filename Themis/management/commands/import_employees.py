import pandas as pd
from dateutil import parser
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from pypinyin import lazy_pinyin
from tqdm import tqdm

from Themis.models.employee import Employee, Degree
from Themis.models.operation import Area
from Themis.models.position import Position, Department


def convert_date(key, row):
    try:
        date = row.get(key).strftime('%Y-%m-%d')
    except Exception as e:
        date = row.get(key)
    return parser.parse(date)


class Command(BaseCommand):
    help = 'Import employees from an Excel file'

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

            department = row.get('department')
            if department:
                # department = str(department)
                # for v in ["华南", "华西", "华东", "AI软件", "新能源"]:
                #     department = department.replace(v, '')
                department, _ = Department.objects.get_or_create(name=department)
                if _:
                    print(f'created {department}')

            position = row.get("position")
            if position:
                position, _ = Position.objects.get_or_create(title=position)
                if _:
                    print(f'created {position}')

            degree = row.get('degree')
            if degree:
                degree, _ = Degree.objects.get_or_create(degree=degree)
                if _:
                    print(f'created {degree}')

            # 创建员工 已有字段

            name = row.get('name')
            employee_number = row.get('employee_number')
            username = "".join(lazy_pinyin(name))
            password = row.get('password')
            date_joined = convert_date('date_joined', row)
            salary_place = row.get('salary_place')
            work_place = row.get('work_place')
            contract_place = row.get('contract_place')
            contract_renewed_times = row.get('contract_renewed_times')
            contract_start_date = convert_date('contract_start_date', row)
            contract_end_date = convert_date('contract_end_date', row)
            insurance_place = row.get('insurance_place')
            bank_number = row.get('bank_number')
            bank_address = row.get('bank_address')
            gender = row.get('gender')
            if not gender == '男' and not gender == '女':
                gender = '未知'
            status = row.get('status')
            expertise = row.get('expertise')
            avatar = 'avatars/default.png'
            phone = row.get('phone')
            id_number = row.get('id_number')
            id_address = row.get('id_address')
            graduated_from = row.get('graduated_from')

            email = username + '@dihuge.com'

            employee = Employee.objects.create(
                name=name,
                last_name=name[0],
                first_name=name[1:],
                username=username,
                employee_number=employee_number,
                position=position,  # foreign key
                department=department,  # foreign key
                area=area,  # foreign key
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
                email=email,
                avatar=avatar,
                bank_address=bank_address,
            )
            print(password)
            employee.password = make_password(str(password))
            employee.save()

            print(f'name:{employee.name}, pwd:{password}')
