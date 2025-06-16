# Plan for Implementing Remaining Core Pillars

## 1. Bilingual Support (Amharic | English)

**Goal**: Enable the application to display content in both Amharic and English, allowing users to switch between languages.

**Sub-tasks**:

- **Django Internationalization (i18n) Setup**:
  - Configure `LANGUAGE_CODE`, `USE_I18N`, and `USE_L10N` in `settings.py`.
  - Add `LocaleMiddleware` to `MIDDLEWARE`.
  - Define `LOCALE_PATHS` to specify where translation files will be stored.
- **Mark Strings for Translation**:
  - Identify all user-facing strings in templates, Python code (views, forms, models), and JavaScript.
  - Wrap these strings with `{% trans "..." %}` or `gettext_lazy()`/`_()` as appropriate.
- **Create Translation Files**:
  - Use `makemessages` Django command to generate `.po` files for Amharic (`am`) and English (`en`).
  - Translate strings in the generated `.po` files.
- **Compile Translation Files**:
  - Use `compilemessages` Django command to compile `.po` files into `.mo` files.
- **Language Switcher Implementation**:
  - Add a language selection mechanism (e.g., dropdown in the header/footer) in `base.html`.
  - Implement a view and URL to set the user's preferred language (e.g., using `set_language` view).

**Key Technologies**: Django's built-in i18n framework.

## 2. Integrated Local Payments (Chapa)

**Goal**: Integrate Chapa payment gateway for local payments.

**Sub-tasks**:

- **Chapa API Integration**:
  - Obtain Chapa API keys (public and secret).
  - Implement a view to initiate a payment (e.g., when a student books a session). This involves making a POST request to Chapa's `/v1/initialize` endpoint with transaction details.
  - Handle Chapa's callback/webhook to verify payment status and update the session status in the database.
- **Payment Model**:
  - Create a `Payment` model to store transaction details (e.g., amount, currency, transaction ID, status, Chapa checkout URL).
- **User Interface for Payment**:
  - Add a "Pay Now" button or similar on the session booking confirmation page.
  - Display payment status to the user.

**Key Technologies**: Python `requests` library for API calls, Chapa API documentation.

## 3. Progress Tracking & Analytics

**Goal**: Implement features to track student progress and provide analytics.

**Sub-tasks**:

- **Data Collection**:
  - Ensure relevant data points are being captured (e.g., session completion, quiz scores, attendance).
  - Modify existing models (e.g., `Session`, `QuizResult`) or create new ones to store detailed progress data.
- **Progress Models**:
  - Consider a `StudentProgress` model that aggregates data (e.g., total sessions, average quiz score, topics covered).
- **Analytics Views and Templates**:
  - Create views to process and present progress data (e.g., `StudentProgressView`).
  - Design a "My Progress" section in the student dashboard to display charts, graphs, and key metrics.
  - For teachers, create a view to see the progress of their students.
- **Reporting**:
  - Implement basic reporting features (e.g., downloadable CSV of session history).

**Key Technologies**: Django ORM for data aggregation, Chart.js or D3.js for data visualization (frontend), potentially Pandas for complex data analysis (backend).

## 4. Real-time Chat

**Goal**: Implement a real-time chat feature between students and tutors.

**Sub-tasks**:

- **Choose a Real-time Technology**:
  - **Django Channels**: Recommended for Django projects.
    - Install and configure Django Channels.
    - Set up `ASGI_APPLICATION` in `settings.py`.
    - Define routing for WebSocket connections.
  - Alternatively, consider third-party services like Pusher, Firebase, or WebSockets directly.
- **Chat Models**:
  - Create `ChatRoom` and `ChatMessage` models to store chat history.
- **Consumers/WebSockets**:
  - Implement Django Channels consumers to handle WebSocket connections, send/receive messages, and broadcast messages to chat room participants.
- **Frontend Integration**:
  - Use JavaScript (e.g., WebSocket API) to establish WebSocket connections and send/receive messages in real-time.
  - Design chat interfaces within the student and tutor dashboards.
- **Notifications**:
  - Integrate chat with the notification system (if implemented) to alert users of new messages.

**Key Technologies**: Django Channels, WebSockets, JavaScript.

## 5. Email/In-app Notifications

**Goal**: Implement a system for sending notifications (e.g., session reminders, verification status updates).

**Sub-tasks**:

- **Notification Model**:
  - Create a `Notification` model (e.g., `recipient`, `message`, `timestamp`, `is_read`, `type`).
- **Email Backend Setup**:
  - Configure Django's email backend in `settings.py` (e.g., SMTP, Console, SendGrid).
- **Notification Triggers**:
  - Identify events that should trigger notifications (e.g., session booked, session cancelled, tutor verified, new message).
  - Implement logic in views or signals to create and send notifications.
- **In-app Notification Display**:
  - Add a notification icon/area in the user's dashboard (e.g., in `base.html` or sidebar).
  - Implement a view to display a list of unread notifications.
- **Email Templates**:
  - Create reusable email templates for different notification types.

**Key Technologies**: Django's `send_mail` or `EmailMessage`, Django signals, custom notification views/templates.

### Implementation Strategy:

- **Iterative Development**: Implement one pillar at a time, testing thoroughly after each.
- **Prioritization**: Start with features that provide immediate value or are prerequisites for others (e.g., Bilingual support might be a good first step for broader user reach).
- **Modular Design**: Keep code for each pillar separate and well-organized within their respective apps (or new apps if complexity warrants).
- **Testing**: Write unit and integration tests for all new functionalities.
