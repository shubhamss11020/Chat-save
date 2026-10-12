---
conversation_id: ddcd59ab-116b-4f78-bd68-045c29f4b38d
platform: claude
username: "shubham"
title: "Running PostgreSQL, Odoo, and n8n with Docker - Claude"
created_at: "2026-10-12T19:04:08.922Z"
updated_at: "2026-10-12 15:04:10 EDT"
---

# Running PostgreSQL, Odoo, and n8n with Docker - Claude

## User (2026-10-12 15:04:10 EDT)

PS C:\Users\vaibhav\Desktop\branon> docker exec -it odoo-db psql -U odoo -d eoxteams -c "select v.id, v.name, v.model, d.module from ir_ui_view v left join ir_model_data d on d.model='ir.ui.view' and d.res_id=v.id where not v.active and v.type='kanban' and v.mode='primary' order by v.model;"  id  |         name         |  model   | module------+----------------------+----------+--------- 4670 | vrm.lead.kanban.lead | vrm.lead | odx_vrm(1 row)

What's next:    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug odoo-db    Learn more at https://docs.docker.com/go/debug-cli/PS C:\Users\vaibhav\Desktop\branon> update ir_ui_view set active=true where id=<us view ki id>;update : The term 'update' is not recognized as the name of a cmdlet, function, script file, or operable program.Check the spelling of the name, or if a path was included, verify that the path is correct and try again.At line:1 char:1+ update ir_ui_view set active=true where id=<us view ki id>;+ ~~~~~~    + CategoryInfo          : ObjectNotFound: (update:String) [], CommandNotFoundException    + FullyQualifiedErrorId : CommandNotFoundException

PS C:\Users\vaibhav\Desktop\branon>

## Claude (2026-10-12 15:04:10 EDT)

Query se ek achhi baat saaf hui. Sirf ek kanban view band hai, vrm.lead.kanban.lead, aur wo odx_vrm module ki hai. Koi standard Odoo view (CRM, Project) galti se band nahi hui, to kuch wapas on karna nahi hai. Is view ko on mat karna, kyunki uska model vrm.lead ab Odoo me hai hi nahi.

PowerShell me jo update ... wali line chali aur error aaya, wo sirf ek SQL ka template tha jo mujhse galti se message me reh gaya. Use terminal me chalane ki zaroorat nahi, aur us error se kuch bigda nahi.

reading 'kanban' error isliye aa raha hai ki ek menu ab bhi vrm.lead ke kanban ko kholne ki koshish kar raha hai, jo exist hi nahi karta. Iska fix un saare menus ko hide karna hai jo missing modules ke hain. Ye command chalao:

docker exec -it odoo-db psql -U odoo -d eoxteams -c "update ir_ui_menu set active=false where id in (select res_id from ir_model_data where model='ir.ui.menu' and (module in ('hr_employee_time_clock','employee_documents_expiry','hr_employee_public_custom','uae_wps_report','eoxs_server_monitor','base_accounting_kit','payment_stripe_recurring_acs','pragtech_team_contact_design','pragtech_lead_stages_exosteam','eoxs_invoice_mail_custom1','m29_project','ringcentral','documents_portal_management','invoice_recurring_acs','sh_account_cancel','web_digital_sign','odx_vrm','account_payment_approval','hr_payslip_monthly_report','theme_clarico_vega') or module like 'emipro_theme%' or module like 'ks_%'));"

Ek aur command, jo in missing modules ke baaki saare views band karti hai (inke fields ab Odoo me nahi hain, to ye aage aur errors rokegi):

docker exec -it odoo-db psql -U odoo -d eoxteams -c "update ir_ui_view set active=false where id in (select res_id from ir_model_data where model='ir.ui.view' and (module in ('hr_employee_time_clock','employee_documents_expiry','hr_employee_public_custom','uae_wps_report','eoxs_server_monitor','base_accounting_kit','payment_stripe_recurring_acs','pragtech_team_contact_design','pragtech_lead_stages_exosteam','eoxs_invoice_mail_custom1','m29_project','ringcentral','documents_portal_management','invoice_recurring_acs','sh_account_cancel','web_digital_sign','odx_vrm','account_payment_approval','hr_payslip_monthly_report','theme_clarico_vega') or module like 'emipro_theme%' or module like 'ks_%'));"

Phir restart karo:

docker restart odoo13

2 minute baad ek hi tab me http://localhost:8069/web?db=eoxteams kholo aur Ctrl+F5 dabao.

Is se kuch menus gayab ho jayenge, jaise Server Monitor, Phonecalls, VRM aur base_accounting_kit ke apne menus. Ye jaan boojhke hai, kyunki unka code is Odoo me hai hi nahi. Standard menus (CRM, Sales, Purchase, Inventory, Project, Employees) rehne chahiye.

Phir bhi koi menu error de, to bata dena ki kaunsa menu tha, aur agar Field ... does not exist wali 2 lines aaye to wo bhej dena.

Ye bhi yaad rakhna: Apps me jaake koi module Upgrade ya Update mat karna.

## User (2026-10-12 15:04:10 EDT)

now create a log note of the work we have done till now in a 2 line bullets and give me 8 bullets the log not should be professional and it should look like it is written by an intern

## Claude (2026-10-12 15:04:10 EDT)

Log Note: MTR Module, n8n and Odoo Setup

Reviewed the MTR Inventory Integration module (Odoo 13) to understand its models, menus and routes. It stores MTR data and inventory records and joins them by heat number and lot number.
Set up PostgreSQL 13, Odoo 13 and n8n with Docker Compose and persistent volumes. Mounted a custom addons folder so Odoo could load the module.
Installed the module and changed the n8n webhook system parameter from the default external URL to the local n8n instance. Confirmed that submitted PDFs reach the n8n Webhook node.
Connected n8n back to Odoo over JSON-RPC (login, then upsert_from_payload on mtr.data). Login works, and the data call reaches Odoo; “record not found” appears only when an old mtr_id is reused.
Fixed a bug in the inventory import where an empty piece_no was written as “False” into an integer column. Wrapped it in the module’s null-handling helper, and the CSV import then went through.
Learned that “Pending” means the PDF was sent to n8n and the extracted data has not come back yet. Prepared importable n8n workflows (a test version and a Claude-based PDF extraction version) to avoid the Fixed/Expression field errors.
Restored the Eoxteams PostgreSQL 12 dump into a separate database (eoxteams) with pg_restore. Confirmed it is Odoo 13.0.1.3, and disabled the cron jobs and mail servers on the local copy for safety.
Fixed errors caused by missing third-party modules (Emipro theme, Ksolves, odx_vrm) by deactivating their views and menus. Next steps: get the extra-addons folder from the EOXS team and test the automatic mtr_id flow end to end.
