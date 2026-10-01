# Student Registration Webpage with GitHub Actions & Jenkins CI/CD

This project contains a student registration form along with continuous integration (CI) pipelines configured for both **GitHub Actions** and **Jenkins** to automatically verify:
1. That `index.html` exists in the repository.
2. That all required form elements and inputs (Full Name, Email, DOB, Gender, Phone, Course, Address, Submit/Reset buttons) are present and valid.

---

## 📁 Project Structure

```text
├── index.html                   # Student Registration Form HTML page
├── Jenkinsfile                  # Jenkins Declarative Pipeline script
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI Workflow configuration
├── tests/
│   └── test_form.py             # Automated unit tests for HTML validation
└── README.md                    # Project documentation & setup instructions
```

---

## 🚀 1. Local Testing

You can run the automated tests locally using Python (no third-party dependencies required):

```bash
# Run tests using Python unittest
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## ⚙️ 2. GitHub Actions Setup

The GitHub Actions workflow is defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

- **Trigger:** Automatically runs on every `push` and `pull_request` to `main` or `master` branches.
- **Workflow Steps:**
  1. Checks out repository code via `actions/checkout@v4`.
  2. Sets up Python via `actions/setup-python@v5`.
  3. Verifies `index.html` exists.
  4. Runs the automated test suite (`tests/test_form.py`).

---

## 🛠️ 3. Jenkins Setup Guide

The pipeline is defined in [`Jenkinsfile`](Jenkinsfile).

### Steps to configure Jenkins:
1. **Create a Pipeline Job:**
   - Open Jenkins Dashboard -> **New Item**.
   - Enter a name (e.g., `student-registration-ci`) and select **Pipeline**.
   - Click **OK**.

2. **Configure Pipeline from SCM:**
   - Scroll down to the **Pipeline** section.
   - Set **Definition** to `Pipeline script from SCM`.
   - Set **SCM** to `Git`.
   - Enter your repository URL (e.g., `https://github.com/<your-user>/<repo-name>.git`).
   - Specify branch specifier: `*/main` or `*/master`.
   - Ensure **Script Path** is set to `Jenkinsfile`.

3. **Set up GitHub Push Trigger (Optional / Recommended):**
   - Under **Build Triggers**, check **GitHub hook trigger for GITScm polling**.
   - In your GitHub Repository settings:
     - Navigate to **Settings** > **Webhooks** > **Add webhook**.
     - Set Payload URL: `http://<YOUR_JENKINS_HOST>:8080/github-webhook/`.
     - Set Content type: `application/json`.
     - Select **Just the push event**.

4. **Run Build:**
   - Click **Build Now** to trigger the build manually or push a commit to trigger it automatically.
