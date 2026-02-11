# Platform Engineering Capstone Project

## Overview

This repository contains the capstone project for our Platform Engineering bootcamp.  
The goal of the project is to build a platform that allows users to run Ansible playbooks against a z/OS mainframe in a reliable, observable, and GitOps-driven way.

**Contributors**

- Ali  
- Anne  
- Apollo  

## High-Level Architecture

At a high level, the platform consists of:

1. **Ansible Control Node**
   - Runs Ansible playbooks targeting a **z/OS mainframe**.
   - Hosted on an **Amazon EC2 instance**.
   - Acts as the main automation entry point for interacting with z/OS.

2. **Monitoring & Observability**
   - The EC2-based Ansible control node is monitored using:
     - **Prometheus** for metrics collection.
     - **Grafana** for dashboards and visualization.
   - This monitoring stack runs on a **Kubernetes** cluster.

3. **GitOps with Argo CD**
   - The monitoring stack (Prometheus, Grafana and related Kubernetes resources) is deployed and managed using **Argo CD**.
   - Argo CD continuously reconciles the desired state (stored in Git) with the actual state of the Kubernetes cluster.

## Components

### 1. Ansible Control Node (EC2)

- Lives on an **AWS EC2** instance.
- Hosts:
  - Ansible and required collections/roles to interact with **z/OS**.
  - Playbooks that define automation workflows for the mainframe.
- Responsibilities:
  - Execute playbooks against z/OS.
  - Expose metrics or logs that can be scraped or collected by the monitoring stack.

### 2. z/OS Mainframe Target

- Acts as the **remote target** for Ansible playbooks.
- Receives configuration, automation tasks, and operations defined in the playbooks.
- The platform is designed so that:
  - z/OS can be managed using standard Ansible workflows.
  - Changes and operations are automated and repeatable.

### 3. Kubernetes-based Monitoring Stack

- Runs on a **Kubernetes cluster**.
- Includes:
  - **Prometheus**: Scrapes metrics from the EC2-based control node and other relevant endpoints.
  - **Grafana**: Visualizes metrics and provides dashboards for:
    - Health and performance of the EC2 instance.
    - Ansible playbook activity and success/failure signals (where exposed).
- Goals:
  - Provide insight into the automation platform’s health.
  - Make it easy to troubleshoot failures or performance issues.

### 4. GitOps with Argo CD

- **Argo CD** is used to deploy and manage:
  - Prometheus and Grafana.
  - Supporting Kubernetes resources (namespaces, ConfigMaps, Secrets, etc.).
- Git is treated as the **source of truth**:
  - Kubernetes manifests and Helm charts are stored in the repository.
  - Argo CD continuously syncs the cluster state with the Git-defined configuration.
- Benefits:
  - Auditable configuration changes.
  - Easy rollbacks and reproducible environments.
  - Declarative deployment of the monitoring stack.

## Data & Control Flow

1. **Developer / Operator Workflow**
   - Write or update Ansible playbooks that target z/OS.
   - Commit changes to Git (playbooks, inventory, or supporting config) as needed.

2. **Running Ansible Playbooks**
   - From the **Ansible control node on EC2**, playbooks are executed against the **z/OS mainframe**.
   - The control node is responsible for authentication, connectivity, and orchestration.

3. **Observability**
   - The EC2 instance exposes metrics and/or logs.
   - **Prometheus** (running in Kubernetes) scrapes these metrics.
   - **Grafana** displays dashboards built on top of Prometheus data, providing:
     - Resource utilization of the EC2 instance.
     - Automation job trends (to the extent metrics are available).
     - Basic health and availability indicators.

4. **GitOps Reconciliation**
   - Any change to the monitoring stack is made via Git (manifests, Helm values, etc.).
   - **Argo CD** detects changes and updates the Kubernetes cluster accordingly.
   - Argo CD continuously ensures the live cluster matches what is defined in Git.

## Project Goals

This capstone is designed to demonstrate:

- **Platform Thinking**
  - Treating the automation system (Ansible + z/OS) as a platform with clear interfaces.
- **Infrastructure as Code & GitOps**
  - Using Git as the single source of truth for Kubernetes resources.
  - Managing deployments through Argo CD rather than manual `kubectl` commands.
- **Observability**
  - Implementing monitoring and dashboards so the platform can be operated confidently.
- **Mainframe Integration**
  - Showing how modern DevOps tooling (Ansible, Kubernetes, Prometheus, Grafana, Argo CD) can integrate with **z/OS mainframes**.

## How This Fits a Real-World Platform

In a real-world environment, this approach provides:

- A centralized, automated way to manage z/OS using Ansible.
- A monitored and observable control plane so that failures and bottlenecks are visible.
- A GitOps-managed monitoring layer that is easy to reproduce across environments (dev, test, prod).
- A foundation that can be extended with:
  - Self-service interfaces (e.g., portals or pipelines to trigger playbooks).
  - Additional automation for other infrastructure or application components.

---
