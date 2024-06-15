from pypdf import PdfReader
import json

reader = PdfReader("Naukri_PrashantMallick.pdf")
text = "".join([page.extract_text(extraction_mode="layout") for page in reader.pages])

with open("temp.json", "w") as f:
    f.write(json.dumps(
        {"resume-text": text, "jd-text": """
SharePoint Developer

Role Description
Responsible for designing, developing, and maintaining SharePoint applications and solutions for various business needs. The SharePoint developer works with different groups at Jefferies to provide the best usability of SharePoint to end users. The SharePoint developer should administer, configure, and support OneDrive for Business, SharePoint environments, including SharePoint Online and SharePoint 2016, Subscription edition. The SharePoint developer has strong skills and experience in SharePoint development, web development, and database development.
Responsibilities
-	Architect, develop and maintain new and existing custom SharePoint applications for different groups at Jefferies to provide best usability of SharePoint to end users
-	Work on administration, security, and governance of SharePoint Online and SharePoint 2016/Subscription
-	Manage overall security of SharePoint Online sites and OneDrive with Information Barriers policies and segments
-	Migrate site structure and content from existing SharePoint 2016 environment to SharePoint Online using Quest/Metalogix Content matrix tool
-	Administer, maintenance and production support of SharePoint 2016 farm in Dev, QA and production environments involving database servers, application servers, web front end servers and office online servers
-	Regular check and upgrade for patches and cumulative updates for all SharePoint 2016 environments (QA & Prod), Data Protection Manager, Office Online Servers using PowerShell scripts
-	Manage and check overall health and functionality of all servers in the farm. Review events and logs in Event Viewer and Performance Monitor. Regular review, clean-up, management and configuration of SharePoint sites, accounts and databases
-	Knowledge in custom InfoPath forms and workflows using SharePoint designer and Workflow Manager

Required Qualifications
-	At least 7 years of experience in SharePoint development, administration, security, and migration
-	At least 3 years of experience in .NET development, web development, and database development
-	Strong knowledge of SharePoint Online, SharePoint 2016, and Subscription
-	Some experience / knowledge of SharePoint server-side and client-side object models, web parts, workflows, event receivers, timer jobs, site definitions, page layouts, content types, site columns, list definitions, and list pages
-	Strong knowledge of SQL Server databases, SQL queries, stored procedures, and triggers
-	Strong knowledge of PowerShell scripts, SharePoint Designer, and Metalogix tool
-	Strong knowledge of web development technologies, such as HTML, CSS, JavaScript, JQuery, and AJAX
-	Strong knowledge of business analysis, requirement gathering, and gap analysis
-	Strong communication, presentation, and interpersonal skills
-	Fast learner, individual as well as a team player and can work under pressure
-	Power Apps and Power Automate development experience would be a plus
-	Certification in SharePoint development or administration is a plus
"""},
        indent=2,
    ))
