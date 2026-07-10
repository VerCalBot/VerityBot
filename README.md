# **VerityBot**
VerityBot is a robust, software solution intended for users who want to make informed security decisions. Using digital sensor data from Verkada -- a premier physical security platform, our application provides detailed, analytical insights into your Verkada system. It is portable, reliable, data-driven, and allows users to feel confident in making important security decisions.

## Requirements
| Requirement                             | Installation                         |
| --------------------------------------- | ------------------------------------ |
| Docker Desktop                          | [Download Here](https://www.docker.com/products/docker-desktop/)     |
| WSL                                     | Prompted during Docker install       |



### <a name="install-and-build">Install & Build 🛠️</a>

Follow this [guide](https://docs.docker.com/desktop/features/wsl/) to set up Docker Desktop and WSL2
<img src="./docs/README-Images/WSL&Docker.png" alt="WSL & Docker" title="WSL & Docker">

Clone the VerityBot git repository into the WSL2 terminal
```git clone git@github.com:VerCalBot/VerityBot.git```

### <a name="Microsoft 365 email setup">Microsoft 365 email setup 📧</a>

VerityBot emails the Kibana dashboard link on a schedule. Because Microsoft 365
has **disabled Basic Authentication (username/password) for SMTP**, VerityBot
authenticates to Microsoft 365 using **OAuth2 with an app registration**
(app-only / client-credentials flow, using a **certificate**). No mailbox
password is used or stored.

You must complete the steps below **before** running `initial_setup.sh`, because
the setup dialogue box asks for the **Tenant ID**, **Client ID**, and
**Certificate Path** produced here. These steps require a **Microsoft 365 /
Entra ID administrator**.

> The exact wording of some portal buttons changes over time; the resource names
> (`Office 365 Exchange Online`, permission `SMTP.SendAsApp`, scope
> `https://outlook.office365.com/.default`) are the parts that matter.

#### 1. Choose or create the sender account
Pick the mailbox that reports will be sent *from* (this is the `Email Sender`
value in the dialogue box). This can be a normal licensed user or, preferably, a
dedicated **service account** / **shared mailbox** (e.g. `veritybot@yourdomain`).
It must have an Exchange Online mailbox.

#### 2. Register an application in Microsoft Entra ID
1. Go to the [Microsoft Entra admin center](https://entra.microsoft.com) →
   **Identity → Applications → App registrations → New registration**.
2. Name it (e.g. `VerityBot Email Sender`), leave redirect URI empty, and
   register. (No redirect URI / SSO is needed for app-only auth.)
3. On the app **Overview** page, copy the **Directory (tenant) ID** and the
   **Application (client) ID** — these become `AZURE_TENANT_ID` and
   `AZURE_CLIENT_ID`.

#### 3. Grant the SMTP send permission (admin consent required)
1. In the app, go to **API permissions → Add a permission → APIs my
   organization uses**, and search for **Office 365 Exchange Online**.
2. Choose **Application permissions**, select **`SMTP.SendAsApp`**, and add it.
3. Click **Grant admin consent for &lt;tenant&gt;** and confirm the permission
   shows a green "Granted" status.

#### 4. Create and upload a certificate
Generate a self-signed certificate on the machine that will run VerityBot (in
WSL). This produces two files: a **private key + certificate** PEM that stays on
the VerityBot host, and a **public certificate** (`.crt`) that you upload to
Entra.

```bash
# Creates veritybot.key (private key), veritybot.crt (public cert), valid 2 years.
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout veritybot.key -out veritybot.crt \
  -days 730 -subj "/CN=VerityBot Email Sender"

# Combine the private key + certificate into one PEM for VerityBot to load.
cat veritybot.key veritybot.crt > veritybot.pem
chmod 600 veritybot.key veritybot.pem   # keep the private key readable only by you
```

1. In the app, go to **Certificates & secrets → Certificates → Upload
   certificate**, and upload **`veritybot.crt`** (the public cert only — never
   upload the `.key` or `.pem`).
2. Note the absolute path to **`veritybot.pem`** on the VerityBot host — this is
   the `Certificate Path` you enter in the dialogue box (`AZURE_CERT_PATH`).
   > Certificates expire (2 years above). Before the expiry date, generate a new
   > cert, upload the new `.crt`, and re-run the setup dialogue box (or just
   > point `AZURE_CERT_PATH` at the new `.pem`), or the nightly email will start
   > failing. Choose a longer `-days` value if you prefer fewer rotations.

#### 5. Scope the app to the sender mailbox and enable SMTP AUTH
This restricts the app so it can only send as your sender mailbox, and ensures
SMTP client submission is allowed for that mailbox. Run these in
[Exchange Online PowerShell](https://learn.microsoft.com/powershell/exchange/connect-to-exchange-online-powershell)
as an Exchange administrator:

> **Is there a web UI for this instead?** Mostly no. `New-ServicePrincipal`
> (registering the app in Exchange) and granting that service principal
> `FullAccess` to the mailbox are **PowerShell-only** — Microsoft provides no
> admin-center UI for them, and the Exchange delegation picker only lists users
> and groups, not app service principals. The **last** command, enabling
> Authenticated SMTP, *does* have a UI: Microsoft 365 admin center →
> **Users → Active users** → select the sender account → **Mail** →
> **Manage email apps** → check **Authenticated SMTP** → **Save changes**.

```powershell
Connect-ExchangeOnline

# Register the app's service principal in Exchange Online.
# AppId  = Application (client) ID from step 2.
# ObjectId = the *Enterprise application* Object ID for this app
#            (Entra → Enterprise applications → your app → Object ID).
New-ServicePrincipal -AppId <AZURE_CLIENT_ID> -ObjectId <ENTERPRISE-APP-OBJECT-ID> -DisplayName "VerityBot Email Sender"

# Allow the app to send only as the sender mailbox.
Add-MailboxPermission -Identity "veritybot@yourdomain.com" -User <ENTERPRISE-APP-OBJECT-ID> -AccessRights FullAccess

# Make sure SMTP AUTH is enabled for the sender mailbox.
Set-CASMailbox -Identity "veritybot@yourdomain.com" -SmtpClientAuthenticationDisabled $false
```

> If your tenant disables SMTP AUTH org-wide (the default), the per-mailbox
> `Set-CASMailbox` override above re-enables it for just this one mailbox.

#### 6. Confirm the sender domain is mapped
VerityBot connects to `smtp.office365.com` for Microsoft 365 domains. If your
sender domain is not already listed in `domain_to_server_mapping` in
`src/email_sender.py`, add it there mapping to `office365.com`.

You now have the three values the dialogue box needs:

| Dialogue box field | Value from above                       | `.env` key        |
| ------------------ | -------------------------------------- | ----------------- |
| Tenant ID          | Directory (tenant) ID (step 2)         | `AZURE_TENANT_ID` |
| Client ID          | Application (client) ID (step 2)       | `AZURE_CLIENT_ID` |
| Certificate Path   | Path to `veritybot.pem` (step 4)       | `AZURE_CERT_PATH` |

### <a name="Initial Setup">Initial Setup 🧑‍💻</a>
Ensure that Docker Desktop is open and running on your host machine \
<img src="./docs/README-Images/DockerRunning.png" alt="Docker Running" title="Docker Running">

Search for WSL in Windows and open it
<img src="./docs/README-Images/OpenWSL.gif" alt="Open WSL" title="Open WSL">

Navigate to ```VerityBot/scripts``` and run ```./initial_setup.sh``` \
<img src="./docs/README-Images/InitialSetup.png" alt="Initial Setup" title="Initial Setup">

If prompted, confirm you would like to delete existing Cron jobs \
<img src="./docs/README-Images/Cron.png" alt="Initial Setup" title="Initial Setup">

When prompted, enter your User password \
<img src="./docs/README-Images/UserPassword.png" alt="User Password" title="User Password">

Enter your credentials into the popup dialogue box
**Note**: All fields must be filled, use the ```Generate Key``` button to create a Kibana Encryption Key.
**Note**: All passwords must be at least 6 characters long.
**Note**: The ```Tenant ID```, ```Client ID```, and ```Certificate Path``` fields come from the [Microsoft 365 email setup](#microsoft-365-email-setup) steps above. \
<img src="./docs/README-Images/DialogueEntry.gif" alt="Dialogue Box" title="Dialogue Box">

Click ```Save``` and exit the popup box \
<img src="./docs/README-Images/DialogueSave.gif" alt="Dialogue Box" title="Dialogue Box">

When prompted, confirm you would like to continue and enter the password for ```kibana_system```. 
**Note**: This should be the same password as the one you placed in the popup for ```Kibana Password```. \
<img src="./docs/README-Images/KibanaPrompt.png" alt="Kibana Prompt" title="Kibana Prompt">

When you see *Setup Complete*, wait until the containers finish starting. 

Use ```docker compose ps``` or view Docker Desktop to check each containers status.
**Note**: The *etl_json* container will  \
<img src="./docs/README-Images/Containers.png" alt="Containers" title="Containers">

Once containers are fully running, then open Kibana. \
```https://localhost:5601```

log in with the following: \
Username: elastic \
Password: The password you set in the popup box for ```Elastic Password``` \
<img src="./docs/README-Images/Elastic.gif" alt="Project Structure" title="Project Structure">


### <a name="Troubleshooting">Troubleshooting 🚧</a>
Force quitting Docker Desktop and reopening it has been found to fix a variety of problems with VerityBot.

### <a name="Project Structure">Project Structure 🏗️</a>
<img src="./docs/README-Images/Workflow.png" alt="Project Structure" title="Project Structure">
