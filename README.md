# DEVSTREAM

## Overview

This project showcases a FastAPI application for managing AWS resources like **RDS snapshots** and **S3 buckets**, using technologies such as HTMX, Jinja2, Tailwind CSS, and Celery. It demonstrates how to build an efficient web interface to manage cloud infrastructure across multiple AWS accounts.

### Key Features

- **AWS Account Management**: Add and manage AWS accounts with role assumptions for cross-account operations.
- **RDS Snapshot Management**: Copy and share RDS and RDS Cluster snapshots across AWS accounts and regions.
- **S3 Bucket Management**: Create S3 buckets in multiple AWS accounts with customizable access policies.
- **HTMX Integration**: Seamless, partial page updates using HTMX for responsive user interaction.
- **Celery + Redis**: Handle long-running background tasks like snapshot copying/sharing asynchronously.

### Technologies Used

1. **FastAPI**: High-performance Python framework for building APIs.
2. **HTMX**: JavaScript library that simplifies dynamic content updates via AJAX.
3. **Jinja2**: Template engine for dynamic HTML generation.
4. **Tailwind CSS + DaisyUI**: Utility-first CSS framework combined with UI components for modern designs.
5. **Celery**: Distributed task queue used for background jobs, like snapshot and bucket creation.
6. **Redis**: Message broker used by Celery for task management.
7. **Docker**: Containerization of the app and its dependencies.

### Features in Depth

#### **1. AWS Account Management**
   Manage multiple AWS accounts, enabling role-based cross-account operations. Accounts are stored in a database with associated role ARNs and environment details.

#### **2. RDS Snapshot Management**
   - Copy RDS and RDS Cluster snapshots to different AWS regions/accounts.
   - Share snapshots by modifying snapshot attributes to enable sharing with other AWS accounts.

#### **3. S3 Bucket Management**
   - Create new S3 buckets in multiple AWS accounts.
   - Choose the bucket name, region, encryption type (S3 or KMS), and apply an access policy generated from a Jinja2 template.

### Project Structure

The app follows a modular structure, with dedicated directories for each feature:

- **app/snapshots**: Contains logic for RDS snapshot copying and sharing.
- **app/s3_buckets**: Logic for S3 bucket creation.
- **app/core**: Shared utilities for handling AWS account management, role assumption, and environment settings.

### Setup

#### 1. **Install Dependencies**

Install all project dependencies using **Poetry**:

```bash
poetry install
```

#### 2. **Docker Setup**

For local development:

```bash
docker-compose -f docker-compose.local.yml up --build
```

For production setup:

```bash
docker-compose -f docker-compose.prod.yml up --build
```

#### 3. **Makefile Commands**

- **build**: `make build` to build the Docker image.
- **up**: `make up` to start the application.
- **down**: `make down` to stop the application.
- **tests**: `make tests` to run all unit tests.

### AWS Services

The app integrates multiple AWS services for managing cloud resources:

#### **Snapshots**
   - **Create** and **copy** snapshots to different regions or accounts.
   - **Share** RDS snapshots with other AWS accounts.
   - AWS clients and role assumptions are handled via shared utility methods.

#### **S3 Bucket Creation**
   - Users can create S3 buckets across AWS accounts with either S3-managed or KMS-managed encryption.
   - Bucket access policies are dynamically generated based on Jinja2 templates.

### UI & Forms

The application uses HTMX to enhance interactivity with partial page loads. Each form in the app is designed to be user-friendly:

#### **Snapshots Form**
   Allows users to input snapshot ID, target AWS account, target region, and optional KMS encryption.

#### **S3 Bucket Form**
   Presents options to select an AWS account, region, bucket name, encryption type, and optional KMS alias.

### Testing & Performance

- **Locust**: Used for load testing.
- **Playwright**: Used for E2E testing with integrated Docker commands.

#### **Running Tests**

To run the tests, use:

```bash
make tests
```

For end-to-end tests:

```bash
make e2e-tests
```

### Security & CORS

The app ensures secure handling of AWS operations, including role assumptions for cross-account access. Additionally, CORS protection is enabled to control resource sharing across different web domains.

