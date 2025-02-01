# Odoo Custom Modules Repository

This repository contains custom Odoo modules developed to enhance the **Purchases Application** and implement a **National ID Processing System**. The repository includes the following modules:

1. Custom Purchase: Extends Odoo's Purchases module by adding RFQ-to-Vendor and bidding functionalities.

2. Purchase Request: Enables employees to submit purchase requests to the Procurement department.

3. National ID Application: Provides a web-based interface for submitting and processing national ID applications.

## Module Breakdown

### 1. Custom Purchase

**Module Name**: custom_purchase

**_Features_**

- Assigns an RFQ to multiple vendors.

- Allows vendors to submit bids linked to an RFQ.

- Implements bid selection and conversion into a Purchase Order.

- Extends the Purchases module UI to support these functionalities.


### 2. Purchase Request

**Module Name**: purchase_request

**_Features_**

- Enables employees to send purchase requests.

- Adds approval workflow for Procurement department.

- Facilitates RFQ creation from purchase requests.


### 3. National ID Application

**Module Name**: id_application

**_Features_**

- Web-based application for national ID submission.

- Allows applicants to upload required documents.

- Implements an approval workflow.

- Logs approval history in the chatter window.


## Usage Instructions

### Creating an RFQ with Multiple Vendors

1. Go to Purchases > Requests for Quotation.

2. Create a new RFQ and select multiple vendors.

3. Send the RFQ and await vendor bids.

### Submitting a Purchase Request

1. Employees can navigate to Purchase Requests and submit requests.

2. The Procurement team reviews and approves requests.

3. Approved requests can be converted into RFQs.

### National ID Application Process

1. Applicants submit an online form with required attachments.

2. The backend tracks approvals from stage 1 to approved/ denied stage.

3. User can also track the status of their application

4. Approvers’ actions are logged in the chatter window.




