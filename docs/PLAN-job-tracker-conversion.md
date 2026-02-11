# PLAN-job-tracker-conversion.md

## 1. Overview
Convert the existing Voice Dash system into a comprehensive General Contractor/Handyman Job Tracker (Jobber.com clone). The system will serve as a CRM, Job Tracker, and Billing platform, leveraging the Antigravity framework and Supabase.

## 2. Project Type
**WEB** (React/Antigravity + Supabase)

## 3. Success Criteria
1.  **Database**: Complete Supabase schema implemented (Clients, Jobs, Estimates, Invoices, Time Tracking).
2.  **Modules**: Fully functional Client, Job, Scheduling, and Billing modules.
3.  **Dashboards**: Admin and Client portals operating with distinct permissions.
4.  **Integrations**: Google Sheets, Google Calendar, and Stripe integration patterns established.
5.  **Verification**: All unit and integration tests fail-free; UX audit passed.

## 4. Tech Stack
-   **Frontend**: React (Antigravity Framework), Tailwind CSS
-   **Backend**: Supabase (PostgreSQL, Auth, Storage, Edge Functions)
-   **State Management**: React Query / Zustand (Antigravity defaults)
-   **Integrations**: Google Sheets API, Google Calendar API, Stripe
-   **PDF Generation**: jsPDF

## 5. File Structure
```
src/
├── components/
│   └── antigravity/       # Core UI components
├── modules/
│   ├── clients/           # Client Management
│   ├── jobs/              # Job Management
│   ├── scheduling/        # Calendar & Appointments
│   ├── billing/           # Estimates & Invoices
│   └── analytics/         # Reporting
├── pages/
│   ├── admin/             # Admin Dashboard Routes
│   └── client/            # Client Portal Routes
└── hooks/                 # Custom hooks (Supabase, Forms)
supabase/
└── migrations/            # SQL Schema definitions
```

## 6. Task Breakdown

### Phase 1: Database & Foundation
**Agent**: `database-architect` / `backend-specialist`

*   **Task 1.1: Client & Job Schema**
    *   **Input**: SQL definitions for `clients`, `jobs`, `job_media`.
    *   **Output**: Migration file `supabase/migrations/01_core_schema.sql` applied.
    *   **Verify**: Table existence and relationship constraints in Supabase.

*   **Task 1.2: Billing & Schedule Schema**
    *   **Input**: SQL definitions for `estimates`, `invoices`, `payments`, `appointments`, `time_entries`.
    *   **Output**: Migration file `supabase/migrations/02_billing_schema.sql` applied.
    *   **Verify**: Foreign keys point correctly to `clients` and `jobs`.

*   **Task 1.3: RLS & Storage**
    *   **Input**: RLS Policies and Storage Bucket definitions (`job-photos`, `invoice-pdfs`).
    *   **Output**: Applied policies for public/private access.
    *   **Verify**: Test unauthorized access blocks (expect 403) and authorized allows (expect 200).

### Phase 2: Client Management Module
**Agent**: `frontend-specialist`

*   **Task 2.1: Client List & DataTable**
    *   **Input**: `ClientList.tsx`, Antigravity `DataTable`.
    *   **Output**: Functional list view with search, filter, and sorting.
    *   **Verify**: Can search for a client and see results.

*   **Task 2.2: Client Form & Details**
    *   **Input**: `ClientForm.tsx`, `ClientDetail.tsx`.
    *   **Output**: Create/Edit functionality and detailed profile view.
    *   **Verify**: Created client appears in DB and List view.

### Phase 3: Job Management Module
**Agent**: `frontend-specialist`

*   **Task 3.1: Job Board & List**
    *   **Input**: `JobBoard.tsx` (Kanban), `JobList.tsx`.
    *   **Output**: Job visualization by status.
    *   **Verify**: Dragging job changes status in DB.

*   **Task 3.2: Job Form & Google Sheets Sync**
    *   **Input**: `JobForm.tsx`, `GoogleSheetsService`.
    *   **Output**: Job creation wizard with auto-sheet generation.
    *   **Verify**: New job creates corresponding Google Sheet row/file.

*   **Task 3.3: Photo Upload & Gallery**
    *   **Input**: `JobPhotoUpload.tsx`, `JobPhotoGallery.tsx`.
    *   **Output**: Drag-drop upload to Supabase Storage.
    *   **Verify**: Uploaded image appears in Gallery and Storage bucket.

### Phase 4: Scheduling Module
**Agent**: `frontend-specialist`

*   **Task 4.1: Calendar Views**
    *   **Input**: `Calendar.tsx`, `DayView.tsx`, `WeekView.tsx`.
    *   **Output**: Interactive calendar grid with appointments.
    *   **Verify**: Appointments render at correct times/dates.

*   **Task 4.2: Appointment Management**
    *   **Input**: `AppointmentForm.tsx`, Drag-and-drop logic.
    *   **Output**: Create/Reschedule functionality.
    *   **Verify**: Moving appointment updates `start_time` and `end_time` in DB.

### Phase 5: Billing Module
**Agent**: `frontend-specialist`

*   **Task 5.1: PDF Service & Templates**
    *   **Input**: `PDFService.ts`, `jsPDF` implementation.
    *   **Output**: Method to generate PDF from Invoice object.
    *   **Verify**: Generated PDF contains correct line items and totals.

*   **Task 5.2: Estimate & Invoice Management**
    *   **Input**: `EstimateEditor.tsx`, `InvoiceEditor.tsx`.
    *   **Output**: CRUD interface for billing documents with calculations.
    *   **Verify**: `subtotal`, `tax`, `total` calculate correctly on line item change.

### Phase 6: Dashboards & Polish
**Agent**: `frontend-specialist`

*   **Task 6.1: Admin Dashboard**
    *   **Input**: `/admin/dashboard` metrics and widgets.
    *   **Output**: Overview page with KPI cards.
    *   **Verify**: Metrics match database counts.

*   **Task 6.2: Client Portal**
    *   **Input**: `/client/*` routes, Estimate approval UI.
    *   **Output**: Secure client view for their specific jobs/invoices.
    *   **Verify**: Client A cannot see Client B's data.

## 7. Phase X: Verification Checklist

- [ ] **Lint & Type Check**: `npm run lint && npx tsc --noEmit`
- [ ] **Security Scan**: Check RLS policies and API endpoints.
- [ ] **Build Check**: `npm run build` succeeds.
- [ ] **UX Audit**: Verify mobile responsiveness of DataTables and Forms.
- [ ] **Manual Test**: Full flow - Create Client -> Create Job -> Schedule -> Invoice -> Pay.
