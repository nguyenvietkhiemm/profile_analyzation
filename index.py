from linkedin_api import Linkedin
import csv
import concurrent.futures

columns = ['profile_id', 'industryName', 'locationName', "experience",
    "education", "languages", "publications", "certifications", "projects", "skills"]

api = Linkedin('', '')

def get_profile(id):
    profile = api.get_profile(id)

    profile = {key: profile[key] for key in columns if key in profile}
    
    if 'experience' in profile:
        experiences = []
        for experience in profile['experience']:
            location = experience.get('locationName', 'N/A')
            company_name = experience.get('companyName', 'N/A')
            title = experience.get('title', 'N/A')
            time_period = experience.get('timePeriod', {})

            start_date = time_period.get('startDate', {})
            end_date = time_period.get('endDate', {})

            start_month = start_date.get('month', '')
            start_year = start_date.get('year', 'N/A')
            end_month = end_date.get('month', '')
            end_year = end_date.get('year', 'N/A')

            # Tạo một dict cho từng trải nghiệm
            experiences.append({
                'title': title,
                'company': company_name,
                'location': location,
                'start_date': f"{start_month}/{start_year}",
                'end_date': f"{end_month}/{end_year}"
            })

        profile['experience'] = experiences

    if 'education' in profile:
        educations = []
        for education in profile['education']:
            school_name = education.get('schoolName', 'N/A')
            degree_name = education.get('degreeName', 'N/A')
            field_of_study = education.get('fieldOfStudy', 'N/A')
            time_period = education.get('timePeriod', {})

            start_year = time_period.get('startDate', {}).get('year', 'N/A')
            end_year = time_period.get('endDate', {}).get('year', 'N/A')

            educations.append({
                'school': school_name,
                'degree': degree_name,
                'field_of_study': field_of_study,
                'start_year': start_year,
                'end_year': end_year
            })

        profile['education'] = educations

    if 'skills' in profile:
        skills = []
        for skill in profile['skills']:
            skill_name = skill.get('name', 'N/A')
            # Tạo một dict cho từng kỹ năng
            skills.append({
                'skill_name': skill_name,
                'standardized_skill': skill.get('standardizedSkill', {}).get('name', 'N/A')
            })

        # Cập nhật profile với thông tin kỹ năng
        profile['skills'] = skills

    if 'publications' in profile:
        publications = []
        for publication in profile['publications']:
            title = publication.get('title', 'N/A')
            publisher = publication.get('publisher', 'N/A')
            date = publication.get('date', 'N/A')
            url = publication.get('url', 'N/A')
            
            if isinstance(date, dict):
                day = date.get('day', '')
                month = date.get('month', '')
                year = date.get('year', '')

                # Đảm bảo rằng day, month, year là kiểu số và định dạng chính xác
                try:
                    formatted_date = f"{(day)}/{(month)}/{(year)}"
                except (ValueError, TypeError):
                    formatted_date = 'N/A'
            else:
                formatted_date = 'N/A'
            
            # Tạo một dict cho từng publication
            publications.append({
                'title': title,
                'publisher': publisher,
                'date': formatted_date,
                'url': url
            })
        
        # Cập nhật profile với thông tin publications
        profile['publications'] = publications

    if 'projects' in profile:
        projects = []
        for project in profile['projects']:
            members = project.get('members', [])
            occupation = members[0]["member"].get("occupation", "N/A") if members else "N/A"

            start_date = project.get('timePeriod', {}).get("startDate", "N/A")
            end_date = project.get('timePeriod', {}).get("endDate", "N/A")
            title = project.get('title', "N/A")
            
            if isinstance(start_date, dict):
                start_day = start_date.get('day', '')
                start_month = start_date.get('month', '')
                start_year = start_date.get('year', '')

                # Đảm bảo rằng day, month, year là kiểu số và định dạng chính xác
                try:
                    formatted_start_date = f"{(start_day)}/{(start_month)}/{(start_year)}"
                    print(formatted_start_date)
                except (ValueError, TypeError):
                    formatted_start_date = 'N/A'
            else:
                formatted_start_date = 'N/A'

            # Chuyển đổi ngày kết thúc thành định dạng dd/mm/yyyy
            if isinstance(end_date, dict):
                end_day = end_date.get('day', '')
                end_month = end_date.get('month', '')
                end_year = end_date.get('year', '')

                # Đảm bảo rằng day, month, year là kiểu số và định dạng chính xác
                try:
                    formatted_end_date = f"{(end_day)}/{(end_month)}/{(end_year)}"
                except (ValueError, TypeError):
                    formatted_end_date = 'N/A'
            else:
                formatted_end_date = 'N/A'

            # Tạo một dict cho từng project
            projects.append({
                'title': title,
                'occupation': occupation,
                'start_date': formatted_start_date,
                'end_date': formatted_end_date
            })
        
        # Cập nhật profile với thông tin projects
        profile['projects'] = projects
        
    if 'certifications' in profile:
        certifications = []
        for certification in profile['certifications']:
            name = certification.get('name', 'N/A')
            authority = certification.get('authority', 'N/A')

            start_date = certification.get('timePeriod', {}).get("startDate", "N/A")
            end_date = certification.get('timePeriod', {}).get("endDate", "N/A")
            
            if isinstance(start_date, dict):
                start_day = start_date.get('day', '')
                start_month = start_date.get('month', '')
                start_year = start_date.get('year', '')

                # Đảm bảo rằng day, month, year là kiểu số và định dạng chính xác
                try:
                    formatted_start_date = f"{(start_day)}/{(start_month)}/{(start_year)}"
                except (ValueError, TypeError):
                    formatted_start_date = 'N/A'
            else:
                formatted_start_date = 'N/A'

            # Chuyển đổi ngày kết thúc thành định dạng dd/mm/yyyy
            if isinstance(end_date, dict):
                end_day = end_date.get('day', '')
                end_month = end_date.get('month', '')
                end_year = end_date.get('year', '')

                # Đảm bảo rằng day, month, year là kiểu số và định dạng chính xác
                try:
                    formatted_end_date = f"{(end_day)}/{(end_month)}/{(end_year)}"
                except (ValueError, TypeError):
                    formatted_end_date = 'N/A'
            else:
                formatted_end_date = 'N/A'
            
            certifications.append({
                'name': name,
                'authority': authority,
                'start_date': formatted_start_date,
                'end_date': formatted_end_date,
            })
        profile['certifications'] = certifications

        
    return profile

columns = ['profile_id', 'industryName', 'locationName', "experience",
           "education", "languages", "publications", "certifications", "projects", "skills"]



def process_profile(row, columns, writer):
    link = row['link']
    title = row["title"]
    id = link.split('/')[-1]

    profile = get_profile(id)
    
    # Chỉ giữ lại các trường trong profile cần thiết
    filtered_profile = {key: profile.get(key, 'N/A') for key in columns}
    filtered_profile['profile_id'] = id  # Thêm profile_id
    filtered_profile['title'] = title  # Thêm title
    
    # Ghi profile vào file
    writer.writerow(filtered_profile)
    print("saved profile", id, "\n")

# Main logic
with open('_data.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ['profile_id', 'title'] + columns[1:]  # Thêm trường title vào sau profile_id
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Ghi tiêu đề cho file

    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Sử dụng ThreadPoolExecutor để thực hiện nhiều get_profile cùng lúc
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for row in reader:
                # Đẩy mỗi tác vụ vào luồng xử lý
                futures.append(executor.submit(process_profile, row, columns, writer))
            
            # Đợi tất cả các tác vụ hoàn thành
            concurrent.futures.wait(futures)




        
