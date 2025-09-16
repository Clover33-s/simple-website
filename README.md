# TikTok Clone

This project is a clone of the TikTok application, built for analysis and demonstration purposes.

## Running the Application

### Prerequisites

- Node.js and npm installed.
- Python and pip installed.

### 1. Install Dependencies

First, install the backend dependencies:

```bash
npm install
```

Then, install the dependencies for the verification script:

```bash
pip install playwright
playwright install
```

### 2. Run the Server

Start the backend server:

```bash
npm start
```

The server will be running at `http://localhost:3000`.

### 3. Verify the Application

You can run the Playwright script to verify that the application is working correctly.

First, make sure you have a `jules-scratch/verification` directory.
Then, you can run the script:

```bash
python jules-scratch/verification/verify_backend.py
```

This will launch a headless browser, navigate to the application, and take a screenshot named `tiktok_clone_backend.png` inside the `jules-scratch/verification` directory.
