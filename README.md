# AI-Powered Data Entry Application

This is a full-stack web application designed for efficient data entry, featuring voice command integration, support for multiple database systems, and containerization with Docker for easy deployment.

## Features

- **Modern Frontend**: A clean and responsive user interface built with HTML, Tailwind CSS, and vanilla JavaScript.
- **Flexible Backend**: A robust backend powered by Flask, providing a stable API for data management.
- **Multi-Database Support**: Connect to either MySQL or MongoDB, with the ability to choose and configure the connection from the UI.
- **Voice-Activated Commands**: Use your voice to fill form fields, submit data, or clear the form, thanks to the integrated Web Speech API.
- **Dockerized Environment**: The entire application is containerized, allowing for a quick and consistent setup using Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the application up and running.

### 1. Clone the Repository

First, clone this repository to your local machine:
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Run with Docker Compose

The simplest way to run the application is with Docker Compose. This command will build the Docker image and start the web server.

```bash
docker-compose up --build
```
The application will be accessible at `http://localhost:5001`.

The `docker-compose.yml` file also includes commented-out service configurations for **MongoDB** and **MySQL**. If you want to run these databases in Docker alongside the application, you can uncomment the relevant sections.

## How to Use the Application

### 1. Connect to a Database

- **Select Database Type**: Choose either "MySQL" or "MongoDB" from the dropdown menu.
- **Provide Connection URI**: Enter the connection string for your database.
  - **MongoDB Example**: `mongodb://host.docker.internal:27017/mydatabase` (if running Mongo locally and the app in Docker).
  - **MySQL Example**: `mysql+pymysql://user:password@host.docker.internal/mydatabase` (if running MySQL locally and the app in Docker).
  - **Note**: `host.docker.internal` is a special DNS name that resolves to the host machine's IP address from within a Docker container.
- **Click Connect**: The status message will confirm whether the connection was successful.

### 2. Add a New Company Record

- **Fill the Form**: Manually type the **Company Name**, **Industry**, and any **Notes** into the input fields.
- **Click "Add Entry"**: The new record will be sent to the database and the table will update automatically.

### 3. Use Voice Commands

Click the **"Voice Command"** button to activate the speech recognition. Your browser may ask for microphone permission.

Here are some example commands:
- **"set company to [Company Name]"**: Fills the "Company Name" field. (e.g., "set company to Innovate Inc")
- **"set industry to [Industry Name]"**: Fills the "Industry" field. (e.g., "set industry to technology")
- **"set notes to [Your Notes]"**: Fills the "Notes" field.
- **"submit data"**: Clicks the "Add Entry" button to save the current record.
- **"clear form"**: Clears all input fields.

After you speak a command, the system will show you what it recognized and execute the corresponding action.