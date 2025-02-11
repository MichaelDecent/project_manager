# Project Manager - Frappe Application

## Overview

**Project Manager** is a custom Frappe application designed to manage projects and tasks. This repository contains the source code and configuration needed to set up and run the application on your local macOS development environment. The application demonstrates a basic Frappe setup, including API development, data management, and other core features.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Install Required Software](#1-install-required-software)
  - [2. Install Bench CLI](#2-install-bench-cli)
  - [3. Initialize a New Bench Instance](#3-initialize-a-new-bench-instance)
  - [4. Create a New Site](#4-create-a-new-site)
  - [5. Create the Custom Application](#5-create-the-custom-application)
  - [6. Install the Application on the Site](#6-install-the-application-on-the-site)
  - [7. Start the Development Server](#7-start-the-development-server)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing the application, ensure your macOS system meets the following requirements:

- **Operating System:** macOS (Mojave or later recommended)
- **Python:** Version 3.6 or higher (macOS usually includes Python 2.7 by default; install Python 3 via Homebrew)
- **Node.js:** Version 12.x or higher
- **Yarn:** Installed via npm or Homebrew
- **Redis:** Installed and running
- **MariaDB (or MySQL):** Installed and running
- **Git:** Installed

### Installing Prerequisites Using Homebrew

If you don't already have Homebrew installed, install it by running:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, install the necessary software:

```bash
# Install Python 3 (if not already installed)
brew install python

# Install Node.js and Yarn
brew install node
brew install yarn

# Install Redis
brew install redis

# Install MariaDB
brew install mariadb

# Start services (you may wish to add these to your startup items)
brew services start redis
brew services start mariadb
```

Ensure Git is installed (Git is usually available with Xcode Command Line Tools):

```bash
xcode-select --install
```

## Installation

Follow these steps to set up the Frappe application from scratch on your macOS.

### 1. Install Bench CLI

Bench is the command-line tool used to manage Frappe applications, sites, and servers. Install it using pip3:

```bash
pip3 install frappe-bench
```

> **Note:** If you encounter permission issues, consider using a virtual environment (recommended) or run the command with `sudo`.

### 2. Initialize a New Bench Instance

Create a new bench instance named `task_frappe_branch`

```bash
bench init task_frappe_branch
cd task_frappe_branch
```

This command sets up the necessary directory structure and installs the core Frappe framework.

### 3. Create a New Site

A Frappe site is where your application will run. Create a new site by running:

```bash
bench new-site task_site.dev
```

During site creation, you will be prompted to enter:
- The MariaDB root password (or the password for your MariaDB user)
- An administrator password for the site

### 4. Create the Custom Application

Now, create your custom application (named `project_manager` in this example):

```bash
bench new-app project_manager
```

You will be prompted to enter:
- **App Name:** (e.g., `project_manager`)
- **App Title:** (e.g., `Project Manager`)
- **App Description:** (e.g., `A project management system built on Frappe`)
- **App Publisher:** (e.g., your name or organization)
- **App Email:** (e.g., your email address)
- **App Version:** (default is fine unless you wish to specify a version)

### 5. Install the Application on the Site

After creating the app, install it on your newly created site:

```bash
bench --site task_site.dev install-app project_manager
```

This command registers your custom application with the site, making it available in the Frappe interface.

### 6. Start the Development Server

Start the bench to launch your site:

```bash
bench start
```

If the site isn't running as expected, you may need to set your site as the current/default site. To force a site to be used as the default site, run:

```bash
bench use task_site.dev
```

Once the server is running, open your web browser and navigate to:

```
http://task_site.dev:8000
```

Log in using the administrator credentials you set up during site creation.

## Usage

- **Frappe Desk:** Use the Frappe desk (dashboard) to manage your application, create DocTypes, and configure your system.
- **Custom Features:** The `project_manager` app folder contains custom modules, API endpoints, and DocTypes that you can modify and extend.
- **API Endpoints:** Custom RESTful API endpoints have been defined for CRUD operations on tasks and projects. Refer to the API documentation within the app for more details.

## Troubleshooting

- **MariaDB Not Found in PATH:**  
  If you encounter an error such as `frappe.exceptions.ExecutableNotFound: mariadb not found in PATH!`, ensure that the MariaDB client is installed and accessible. You might need to add its directory to your system's PATH or create a symbolic link to the `mysql` executable:
  
  ```bash
  sudo ln -s $(which mysql) /usr/local/bin/mariadb
  ```

- **Redis Issues:**  
  Verify that the Redis server is running:

  ```bash
  brew services list
  ```

- **Node.js or Yarn Errors:**  
  Ensure that Node.js and Yarn are correctly installed and that their versions meet the requirements.

- **Site Not Running:**  
  If your site does not load, set it as the current site by running:

  ```bash
  bench use task_site.dev
  ```

- **Permissions Issues:**  
  If you run into permission errors while installing or running commands, consider using a virtual environment or adjusting your user permissions.
