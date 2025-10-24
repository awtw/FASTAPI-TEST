# Custom Swagger UI HTML with dark mode
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse


def custom_swagger_ui_html(*args, **kwargs):
    swagger_ui = get_swagger_ui_html(*args, **kwargs)
    swagger_ui_content = swagger_ui.body.decode()

    return HTMLResponse(content=swagger_ui_content, status_code=200)

    # Inject custom CSS for dark mode with modern styling
    dark_mode_css = """
    <style id="swagger-dark-theme">
    /* Modern Dark Mode Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    body {
        margin: 0;
        padding: 0;
    }

    body, .swagger-ui {
        background-color: #0c1120 !important; /* Deeper, richer background */
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    .swagger-ui .topbar {
        background: linear-gradient(135deg, #1e1b4b, #0f172a) !important; /* More interesting gradient */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        border-bottom: 1px solid #3f3f80 !important; /* More colorful border */
        padding: 10px 0 !important;
    }

    /* Typography Improvements */
    .swagger-ui .info h2.title {
        font-weight: 700 !important;
        font-size: 32px !important;
        color: #f8fafc !important;
        margin-bottom: 20px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important; /* Add subtle text shadow */
    }

    .swagger-ui .info p, 
    .swagger-ui .info li {
        font-size: 15px !important;
        line-height: 1.6 !important;
        color: #cbd5e1 !important;
    }

    .swagger-ui .opblock-tag {
        font-size: 18px !important;
        font-weight: 600 !important;
        border-bottom: 1px solid #4b4f8c !important; /* More colorful border */
        margin: 20px 0 10px 0 !important;
        padding: 10px 0 !important;
        color: #f8fafc !important;
    }

    .swagger-ui .opblock .opblock-summary-operation-id, 
    .swagger-ui .opblock .opblock-summary-path,
    .swagger-ui .opblock .opblock-summary-path__deprecated,
    .swagger-ui .opblock .opblock-summary-description,
    .swagger-ui table thead tr td, 
    .swagger-ui table thead tr th,
    .swagger-ui .tab li,
    .swagger-ui .response-col_status,
    .swagger-ui .response-col_description,
    .swagger-ui .parameter__name,
    .swagger-ui .parameter__type,
    .swagger-ui .parameter__in,
    .swagger-ui label,
    .swagger-ui .responses-inner h4,
    .swagger-ui .responses-inner h5,
    .swagger-ui section.models h4,
    .swagger-ui .model-title,
    .swagger-ui .model {
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Modern Button Styling - Enhanced colors */
    .swagger-ui .btn {
        background: linear-gradient(to bottom, #334155, #1e293b) !important;
        border: none !important;
        color: #f8fafc !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
    }

    .swagger-ui .btn:hover {
        background: linear-gradient(to bottom, #3b4a67, #243351) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }

    .swagger-ui .btn.execute {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
    }

    .swagger-ui .btn.execute:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
    }

    .swagger-ui .try-out__btn {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        color: white !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
    }

    .swagger-ui .try-out__btn:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Operations and Blocks */
    .swagger-ui .opblock {
        background: linear-gradient(to bottom, #1a233b, #151b2f) !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        margin: 0 0 16px 0 !important;
        overflow: hidden !important;
        transition: box-shadow 0.2s ease !important;
        border-left: 3px solid #3b4880 !important; /* Colored left border */
    }

    .swagger-ui .opblock:hover {
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25) !important;
    }

    .swagger-ui .opblock .opblock-section-header {
        background-color: #242c46 !important; /* More vibrant header bg */
        border-bottom: 1px solid #384069 !important;
        padding: 12px !important;
    }

    /* HTTP Methods - Modern Look with improved colors */
    .swagger-ui .opblock-summary-method {
        border-radius: 6px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
        padding: 8px 12px !important;
        margin-right: 12px !important;
    }

    .swagger-ui .opblock-get .opblock-summary-method {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        color: white !important;
    }

    .swagger-ui .opblock-post .opblock-summary-method {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: white !important;
    }

    .swagger-ui .opblock-put .opblock-summary-method {
        background: linear-gradient(135deg, #d97706, #f59e0b) !important;
        color: white !important;
    }

    .swagger-ui .opblock-delete .opblock-summary-method {
        background: linear-gradient(135deg, #dc2626, #ef4444) !important;
        color: white !important;
    }

    .swagger-ui .opblock-patch .opblock-summary-method {
        background: linear-gradient(135deg, #7c3aed, #8b5cf6) !important;
        color: white !important;
    }

    /* Container styling */
    .swagger-ui .scheme-container {
        background: linear-gradient(to bottom, #1e293b, #172033) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        border-radius: 10px !important;
        margin: 16px 0 !important;
        padding: 20px !important;
        border: 1px solid #3b4880 !important; /* Add subtle colored border */
    }

    /* Forms and Inputs - Enhanced colors */
    .swagger-ui select {
        background-color: #252d47 !important;
        color: #f8fafc !important;
        border: 1px solid #4b5399 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        height: auto !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
    }

    .swagger-ui select:focus {
        border-color: #6366f1 !important; /* Indigo accent */
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
    }

    .swagger-ui input[type=text], 
    .swagger-ui textarea {
        background-color: #252d47 !important;
        color: #f8fafc !important;
        border: 1px solid #4b5399 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
    }

    .swagger-ui input[type=text]:focus,
    .swagger-ui textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
        outline: none !important;
    }

    /* Table styling with enhanced colors */
    .swagger-ui table {
        background-color: #17203c !important; /* Richer table bg */
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
        overflow: hidden !important;
    }

    .swagger-ui table thead tr {
        background-color: #242c46 !important; /* More vibrant header */
    }

    .swagger-ui table thead tr th {
        color: #f8fafc !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
    }

    .swagger-ui table tbody tr td {
        border-top: 1px solid #384069 !important; /* More colorful divider */
        padding: 12px 16px !important;
    }

    /* Response Section */
    .swagger-ui .responses-wrapper,
    .swagger-ui .response-col_description__inner {
        background-color: #1e293b !important;
        border-radius: 8px !important;
    }

    .swagger-ui .highlight-code {
        background-color: #0f172a !important;
        border-radius: 8px !important;
        padding: 12px !important;
        border: 1px solid #334155 !important;
    }

    .swagger-ui .responses-inner {
        background-color: #1e293b !important;
        padding: 16px !important;
        border-radius: 8px !important;
    }

    .swagger-ui .example {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }

    .swagger-ui .response {
        background-color: #0f172a !important;
        padding: 16px !important;
        border-radius: 8px !important;
    }

    /* Code examples - enhanced syntax highlighting */
    .swagger-ui .microlight {
        background: linear-gradient(to bottom, #111827, #0c1120) !important;
        color: #f8fafc !important;
        font-family: 'Menlo', 'Monaco', 'Consolas', monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: 1px solid #384069 !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    /* Syntax highlighting enhancements for better readability */
    .swagger-ui .microlight .keyword {
        color: #a78bfa !important; /* Light purple */
        font-weight: 600 !important;
    }

    .swagger-ui .microlight .string {
        color: #34d399 !important; /* Emerald green */
    }

    .swagger-ui .microlight .number {
        color: #fbbf24 !important; /* Amber yellow */
    }

    .swagger-ui .microlight .boolean {
        color: #60a5fa !important; /* Light blue */
        font-weight: 600 !important;
    }

    .swagger-ui .microlight .function {
        color: #f472b6 !important; /* Pink */
        font-weight: 600 !important;
    }

    .swagger-ui .microlight .operator {
        color: #94a3b8 !important; /* Light slate */
    }

    .swagger-ui .microlight .null, 
    .swagger-ui .microlight .undefined {
        color: #f87171 !important; /* Red */
        font-style: italic !important;
    }

    .swagger-ui .microlight .comment {
        color: #64748b !important; /* Slate */
        font-style: italic !important;
    }

    /* Example Value section - improved colors */
    .swagger-ui .example-value-wrapper,
    .swagger-ui .model-example {
        background: linear-gradient(to bottom, #111827, #0c1120) !important;
        border: 1px solid #384069 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    /* Response content type selector - improve styling */
    .swagger-ui .response-content-type {
        background-color: #252d47 !important;
        color: #f8fafc !important;
        border: 1px solid #4b5399 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        height: auto !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        margin-top: 10px !important;
    }

    /* Add subtle page transitions */
    .swagger-ui .opblock-body,
    .swagger-ui .tab-container,
    .swagger-ui .model-box,
    .swagger-ui section.models {
        animation: fadeInContent 0.3s ease-in-out;
    }

    @keyframes fadeInContent {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Add subtle pulsing effect to try-it-out button */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }

    /* Apply pulsing animation to execute button */
    .swagger-ui .btn.execute {
        animation: pulse 2s infinite;
    }

    /* Add subtle separator between endpoints */
    .swagger-ui .opblock-tag-section {
        position: relative;
        padding-bottom: 20px;
    }

    .swagger-ui .opblock-tag-section:not(:last-child)::after {
        content: '';
        position: absolute;
        bottom: 10px;
        left: 20%;
        right: 20%;
        height: 1px;
        background: linear-gradient(to right, transparent, #3b4880, transparent);
    }

    /* Smooth scrolling for page */
    html {
        scroll-behavior: smooth;
    }

    /* Subtle header text shadow for depth */
    .swagger-ui .opblock-summary-operation-id, 
    .swagger-ui .opblock-summary-path,
    .swagger-ui .opblock-summary-path__deprecated,
    .swagger-ui .tab li,
    .swagger-ui section.models h4,
    .swagger-ui .opblock-tag {
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Give opblock headers a subtle gradient background */
    .swagger-ui .opblock .opblock-summary {
        background: linear-gradient(to right, rgba(59, 72, 128, 0.1), rgba(30, 41, 59, 0)) !important;
    }
    
    /* Add custom scrollbar styling */
    .swagger-ui ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    .swagger-ui ::-webkit-scrollbar-track {
        background: #0f172a;
        border-radius: 4px;
    }
    
    .swagger-ui ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    
    .swagger-ui ::-webkit-scrollbar-thumb:hover {
        background: #3b4880;
    }

    /* Enhance the visibility of Parameters and Responses section headers */
    .swagger-ui .opblock-section-header h4 span,
    .swagger-ui .tab li,
    .swagger-ui .response-col_status,
    .swagger-ui .response-col_description {
        color: #f8fafc !important; /* Bright white */
        font-weight: 600 !important;
    }

    /* Make Parameters and Responses headers extra prominent */
    .swagger-ui .opblock-section-header {
        background: linear-gradient(to right, #1e2b45, #141c36) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin-bottom: 16px !important;
        border-left: 4px solid #3b82f6 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }

    .swagger-ui .opblock-section-header h4 {
        color: #ffffff !important; /* Pure white for better visibility */
        font-weight: 700 !important;
        font-size: 16px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4) !important;
        letter-spacing: 0.5px !important;
    }

    /* Add special icon before Parameters and Responses to make them stand out */
    .swagger-ui .opblock-section-header h4:before {
        content: '• ';
        color: #60a5fa !important;
        font-size: 20px !important;
        vertical-align: middle !important;
        text-shadow: 0 0 4px rgba(96, 165, 250, 0.6) !important;
    }

    /* Add a glow effect to highlight the important sections */
    .swagger-ui .parameters-container,
    .swagger-ui .responses-wrapper {
        position: relative !important;
    }

    .swagger-ui .parameters-container:after,
    .swagger-ui .responses-wrapper:after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        border-radius: 8px !important;
        box-shadow: inset 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        pointer-events: none !important;
        z-index: 1 !important;
    }

    /* Parameters table styling */
    .swagger-ui .parameters-col_name {
        font-weight: 700 !important;
        font-size: 14px !important;
        color: #60a5fa !important; /* Brighter blue for better visibility */
    }

    /* Response status code styling */
    .swagger-ui .response-col_status {
        font-weight: 700 !important;
        font-size: 15px !important;
        background: linear-gradient(to bottom, #242c46, #1a233b) !important;
        border-radius: 4px !important;
        padding: 6px 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid #384069 !important;
        min-width: 75px !important;
        text-align: center !important;
    }

    /* Enhance parameter rows for better readability */
    .swagger-ui table.parameters {
        border: 1px solid #384069 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        margin-bottom: 16px !important;
    }

    .swagger-ui table.parameters tr {
        background-color: #171f38 !important;
        border-bottom: 1px solid #2a3555 !important;
        transition: background-color 0.2s ease !important;
    }

    .swagger-ui table.parameters tr:hover {
        background-color: #1e2945 !important;
    }

    .swagger-ui table.parameters tr:last-child {
        border-bottom: none !important;
    }

    .swagger-ui table.parameters tr td {
        padding: 12px !important;
        vertical-align: top !important;
    }

    /* Parameter details */
    .swagger-ui .parameter__name {
        font-family: 'Menlo', 'Monaco', 'Consolas', monospace !important;
        color: #60a5fa !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        display: block !important;
        margin-bottom: 4px !important;
    }

    .swagger-ui .parameter__in {
        color: #94a3b8 !important;
        font-size: 12px !important;
        background-color: #1a233b !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        margin-left: 4px !important;
        border: 1px solid #334155 !important;
    }

    .swagger-ui .parameter__type {
        color: #a5b4fc !important; /* Light purple */
        font-family: 'Menlo', 'Monaco', 'Consolas', monospace !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /* Required parameter badge */
    .swagger-ui .parameter__name.required:after {
        content: "required" !important;
        color: #ffffff !important;
        background: linear-gradient(135deg, #dc2626, #ef4444) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        margin-left: 8px !important;
        vertical-align: middle !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 1px 3px rgba(239, 68, 68, 0.3) !important;
    }

    /* Parameter description styles */
    .swagger-ui .markdown p {
        color: #e2e8f0 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        margin-top: 6px !important;
    }

    /* Response description styles */
    .swagger-ui .response-col_description p {
        color: #e2e8f0 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    .swagger-ui .response-col_description .markdown code {
        background-color: #1a233b !important;
        color: #a5b4fc !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-family: 'Menlo', 'Monaco', 'Consolas', monospace !important;
        font-size: 13px !important;
        border: 1px solid #334155 !important;
    }

    /* ===== AUTHORIZATION PANEL STYLING ===== */
    
    /* Authorization Dialog Styling */
    .swagger-ui .dialog-ux .modal-ux {
        background: linear-gradient(to bottom, #1a233b, #141c36) !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        overflow: hidden !important;
        max-width: 650px !important;
        width: 90% !important;
    }

    .swagger-ui .dialog-ux .modal-ux-header {
        background: linear-gradient(to right, #1e2b45, #141c36) !important;
        border-bottom: 1px solid #3b4880 !important;
        padding: 16px 24px !important;
        display: flex !important;
        align-items: center !important;
    }

    .swagger-ui .dialog-ux .modal-ux-header h3 {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }

    .swagger-ui .dialog-ux .modal-ux-content {
        background-color: #171f38 !important;
        color: #f8fafc !important;
        padding: 24px !important;
    }

    /* Authorization Form Elements */
    .swagger-ui .auth-container {
        padding: 10px !important;
    }

    .swagger-ui .auth-container h4,
    .swagger-ui .auth-container p,
    .swagger-ui .auth-container label,
    .swagger-ui .auth-container .footnote {
        color: #f8fafc !important;
    }

    .swagger-ui .auth-container h4 {
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
        padding-bottom: 8px !important;
        border-bottom: 1px solid #3b4880 !important;
        color: #60a5fa !important;
    }

    .swagger-ui .auth-container label {
        font-weight: 600 !important;
        margin-bottom: 6px !important;
        display: block !important;
        color: #e2e8f0 !important;
    }

    .swagger-ui .auth-container input[type=text],
    .swagger-ui .auth-container input[type=password] {
        background-color: #242c46 !important;
        color: #f8fafc !important;
        border: 1px solid #4b5399 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        width: 100% !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
        font-size: 14px !important;
        margin-bottom: 16px !important;
    }

    .swagger-ui .auth-container input[type=text]:focus,
    .swagger-ui .auth-container input[type=password]:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
        outline: none !important;
    }

    .swagger-ui .auth-btn-wrapper {
        display: flex !important;
        justify-content: flex-end !important;
        padding: 16px 0 !important;
        margin-top: 10px !important;
        border-top: 1px solid #3b4880 !important;
    }

    .swagger-ui .auth-btn-wrapper .btn {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        margin-left: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
    }

    .swagger-ui .auth-btn-wrapper .btn:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
    }

    .swagger-ui .auth-btn-wrapper .btn.modal-btn-cancel {
        background: linear-gradient(to bottom, #4b5563, #374151) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    .swagger-ui .auth-btn-wrapper .btn.modal-btn-cancel:hover {
        background: linear-gradient(to bottom, #64748b, #4b5563) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
    }

    /* Authorize button at the top */
    .swagger-ui .authorization__btn {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
    }

    .swagger-ui .authorization__btn:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
    }

    /* Lock icon */
    .swagger-ui .unlocked,
    .swagger-ui .locked {
        opacity: 1 !important;
    }

    /* OAuth scope section */
    .swagger-ui .scopes {
        padding: 16px !important;
        background-color: #242c46 !important;
        border-radius: 8px !important;
        margin-top: 12px !important;
        border: 1px solid #3b4880 !important;
    }

    .swagger-ui .scope-def {
        padding: 12px !important;
        border-bottom: 1px solid #3b4880 !important;
    }

    .swagger-ui .scope-def:last-child {
        border-bottom: none !important;
    }

    .swagger-ui .scopes h2 {
        color: #f8fafc !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-bottom: 12px !important;
    }

    .swagger-ui .scopes .scope-name {
        color: #60a5fa !important;
        font-family: 'Menlo', 'Monaco', 'Consolas', monospace !important;
        font-size: 14px !important;
    }

    .swagger-ui .scopes .scope-description {
        color: #e2e8f0 !important;
        font-size: 14px !important;
    }
    
    /* Close button */
    .swagger-ui .dialog-ux .modal-ux-header .close-modal {
        transition: all 0.2s ease !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-header .close-modal svg {
        height: 20px !important;
        width: 20px !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-header .close-modal:hover {
        transform: scale(1.2) !important;
    }
    
    /* Security definitions container */
    .swagger-ui .auth-container .security-definition-reference {
        margin-bottom: 20px !important;
        background-color: #1a233b !important;
        padding: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #3b4880 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Scheme name */
    .swagger-ui .auth-container .security-definition-reference .operation-security-definition {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #60a5fa !important;
        margin-bottom: 8px !important;
    }
    
    /* Footer notes */
    .swagger-ui .auth-container .footnote {
        margin-top: 16px !important;
        font-size: 13px !important;
        color: #94a3b8 !important;
        line-height: 1.5 !important;
    }
    
    /* Authentication indicator icons in the UI */
    .swagger-ui .authorization__btn .svg-assets {
        fill: #f8fafc !important;
        color: #f8fafc !important;
    }
    
    /* Improve the appearance of lock icons in operation summary */
    .swagger-ui .opblock-summary-control .authorization__btn {
        padding: 4px !important;
        background: transparent !important;
        box-shadow: none !important;
        margin-right: 5px !important;
    }
    
    .swagger-ui .opblock-summary-control .authorization__btn svg {
        height: 18px !important;
        width: 18px !important;
    }
    
    /* Unlocked icon */
    .swagger-ui .unlocked svg {
        fill: #94a3b8 !important;
    }
    
    /* Locked/authenticated icon */
    .swagger-ui .locked svg {
        fill: #34d399 !important; /* Green for authenticated */
    }
    
    /* Add a subtle glow to authenticated endpoints */
    .swagger-ui .opblock-summary-control .locked {
        position: relative !important;
    }
    
    .swagger-ui .opblock-summary-control .locked::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 22px;
        height: 22px;
        background: radial-gradient(circle, rgba(52, 211, 153, 0.3) 0%, rgba(52, 211, 153, 0) 70%);
        border-radius: 50%;
        z-index: -1;
    }
    
    /* Highlight authenticated endpoints differently */
    .swagger-ui .opblock.opblock-authenticated {
        border-left-width: 4px !important;
    }
    
    /* Adding a badge for authenticated endpoints in summary */
    .swagger-ui .opblock-summary-control .locked::before {
        content: 'Auth';
        position: absolute;
        top: -12px;
        right: -12px;
        background-color: #059669;
        color: white;
        font-size: 9px;
        font-weight: bold;
        padding: 2px 4px;
        border-radius: 4px;
        opacity: 0;
        transform: scale(0.8);
        transition: all 0.2s ease;
    }
    
    .swagger-ui .opblock-summary-control .locked:hover::before {
        opacity: 1;
        transform: scale(1);
    }
    
    /* ===== ADDITIONAL AUTH CONTROL ELEMENTS ===== */
    
    /* Styling for checkbox and radio inputs */
    .swagger-ui .auth-container input[type=checkbox],
    .swagger-ui .auth-container input[type=radio] {
        position: relative !important;
        width: 18px !important;
        height: 18px !important;
        margin-right: 8px !important;
        cursor: pointer !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
        border: 2px solid #4b5399 !important;
        border-radius: 4px !important;
        background-color: #242c46 !important;
        transition: all 0.2s ease !important;
        vertical-align: middle !important;
    }
    
    .swagger-ui .auth-container input[type=checkbox]:checked,
    .swagger-ui .auth-container input[type=radio]:checked {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
    }
    
    .swagger-ui .auth-container input[type=checkbox]:checked::before,
    .swagger-ui .auth-container input[type=radio]:checked::before {
        content: '✓' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        color: #ffffff !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    
    .swagger-ui .auth-container input[type=checkbox]:focus,
    .swagger-ui .auth-container input[type=radio]:focus {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Radio buttons should be round */
    .swagger-ui .auth-container input[type=radio] {
        border-radius: 50% !important;
    }
    
    .swagger-ui .auth-container input[type=radio]:checked::before {
        content: '' !important;
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        background-color: #ffffff !important;
    }
    
    /* Select dropdown styling */
    .swagger-ui .auth-container select {
        background-color: #242c46 !important;
        color: #f8fafc !important;
        border: 1px solid #4b5399 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        width: 100% !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
        font-size: 14px !important;
        margin-bottom: 16px !important;
        cursor: pointer !important;
        appearance: none !important;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2394a3b8'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: right 10px center !important;
        background-size: 20px !important;
        padding-right: 32px !important;
    }
    
    .swagger-ui .auth-container select:focus {
        outline: none !important;
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
    }
    
    .swagger-ui .auth-container select option {
        background-color: #1a233b !important;
        color: #f8fafc !important;
        padding: 10px !important;
    }
    
    /* Custom auth panel subtitles */
    .swagger-ui .auth-container .subtitle {
        color: #94a3b8 !important;
        font-size: 13px !important;
        margin-bottom: 15px !important;
        line-height: 1.5 !important;
    }
    
    /* Auth panel description text */
    .swagger-ui .auth-container p {
        color: #e2e8f0 !important;
        line-height: 1.6 !important;
        margin-bottom: 12px !important;
    }
    
    /* Apply button special styling */
    .swagger-ui .auth-btn-wrapper .btn.authorize {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3) !important;
    }
    
    .swagger-ui .auth-btn-wrapper .btn.authorize:hover {
        background: linear-gradient(135deg, #047857, #059669) !important;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4) !important;
    }
    </style>

    <style id="swagger-light-theme" disabled>
    /* Light mode styling */
    /* ... existing CSS ... */
    </style>
    """

    # Add JavaScript for theme switching and debug mode functionality
    theme_toggle_js = """
    <script>
    window.addEventListener('DOMContentLoaded', (event) => {
        // Create toggle elements
        const topbarRight = document.querySelector('.topbar-wrapper .download-url-wrapper');

        if (topbarRight) {
            // Create container for theme switch
            const switchContainer = document.createElement('div');
            switchContainer.className = 'theme-switch-container';

            // Create dark/light mode text
            const darkText = document.createElement('span');
            darkText.className = 'mode-label';
            darkText.textContent = 'Dark';

            // Create toggle switch
            const themeSwitch = document.createElement('label');
            themeSwitch.className = 'theme-switch';

            const themeInput = document.createElement('input');
            themeInput.type = 'checkbox';
            themeInput.id = 'theme-toggle';

            const slider = document.createElement('span');
            slider.className = 'slider';

            themeSwitch.appendChild(themeInput);
            themeSwitch.appendChild(slider);

            // Create light mode text
            const lightText = document.createElement('span');
            lightText.className = 'mode-label';
            lightText.textContent = 'Light';

            // Create debug mode checkbox
            const debugContainer = document.createElement('div');
            debugContainer.className = 'debug-checkbox';

            const debugInput = document.createElement('input');
            debugInput.type = 'checkbox';
            debugInput.id = 'debug-toggle';

            const debugLabel = document.createElement('label');
            debugLabel.htmlFor = 'debug-toggle';
            debugLabel.textContent = 'Debug Mode';

            debugContainer.appendChild(debugInput);
            debugContainer.appendChild(debugLabel);

            // Create debug info container (initially hidden)
            const debugInfo = document.createElement('div');
            debugInfo.className = 'debug-info';
            debugInfo.id = 'debug-info';

            // Append elements
            switchContainer.appendChild(darkText);
            switchContainer.appendChild(themeSwitch);
            switchContainer.appendChild(lightText);
            switchContainer.appendChild(debugContainer);

            topbarRight.prepend(switchContainer);

            // Add debug info after the topbar
            const mainContainer = document.querySelector('.swagger-ui');
            if (mainContainer) {
                mainContainer.insertBefore(debugInfo, mainContainer.firstChild);
            }

            // Set up event listeners
            themeInput.addEventListener('change', function() {
                toggleTheme(this.checked);
            });

            debugInput.addEventListener('change', function() {
                toggleDebugMode(this.checked);
            });

            // Force dark mode by default - make sure dark theme is always active initially
            const darkTheme = document.getElementById('swagger-dark-theme');
            const lightTheme = document.getElementById('swagger-light-theme');

            // Ensure dark theme is enabled and light theme is disabled by default
            if (darkTheme) darkTheme.disabled = false;
            if (lightTheme) lightTheme.disabled = true;

            // Only check for saved theme after ensuring dark mode is default
            const savedTheme = localStorage.getItem('swagger-theme');
            if (savedTheme === 'light') {
                themeInput.checked = true;
                toggleTheme(true);
            } else {
                // If no saved theme or it's 'dark', make sure dark mode is applied
                localStorage.setItem('swagger-theme', 'dark');
            }

            // Initialize debug info
            updateDebugInfo();
        }

        // Theme toggle function
        function toggleTheme(isLight) {
            const darkTheme = document.getElementById('swagger-dark-theme');
            const lightTheme = document.getElementById('swagger-light-theme');

            if (isLight) {
                darkTheme.disabled = true;
                lightTheme.disabled = false;
                localStorage.setItem('swagger-theme', 'light');
            } else {
                darkTheme.disabled = false;
                lightTheme.disabled = true;
                localStorage.setItem('swagger-theme', 'dark');
            }

            // Update debug info if debug mode is on
            updateDebugInfo();
        }

        // Debug mode toggle function
        function toggleDebugMode(isDebug) {
            const debugInfo = document.getElementById('debug-info');

            if (isDebug) {
                debugInfo.style.display = 'block';
                updateDebugInfo();
            } else {
                debugInfo.style.display = 'none';
            }
        }

        // Update debug info
        function updateDebugInfo() {
            const debugInfo = document.getElementById('debug-info');
            if (!debugInfo) return;

            const currentTheme = localStorage.getItem('swagger-theme') || 'dark';
            const windowSize = `Window: ${window.innerWidth}x${window.innerHeight}`;
            const userAgent = `User Agent: ${navigator.userAgent}`;
            const activeCss = `Active Theme: ${currentTheme}`;
            const apiEndpoints = `API Endpoints: ${document.querySelectorAll('.opblock').length}`;
            const modelCount = `Models: ${document.querySelectorAll('.model-container').length}`;

            debugInfo.innerHTML = `<strong>Debug Information:</strong>
<hr>
${activeCss}
${windowSize}
${userAgent}
${apiEndpoints}
${modelCount}
<hr>
<strong>Element Colors:</strong>
Body BG: ${getComputedStyle(document.body).backgroundColor}
Topbar BG: ${document.querySelector('.topbar') ? getComputedStyle(document.querySelector('.topbar')).backgroundColor : 'N/A'}
Operation BG: ${document.querySelector('.opblock') ? getComputedStyle(document.querySelector('.opblock')).backgroundColor : 'N/A'}
<hr>
<strong>Performance:</strong>
Page Load Time: ${window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart}ms
Resource Count: ${performance.getEntriesByType('resource').length}
`;
        }
    });
    </script>
    """

    # Insert the custom CSS in the head and JavaScript before the closing body tag
    modified_content = swagger_ui_content.replace('</head>', f'{dark_mode_css}</head>')

    # Add hash navigation JavaScript to handle direct endpoint access
    hash_navigation_js = """
    <script>
    // Function to navigate to a specific endpoint based on URL hash
    window.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            // Check if there's a hash in the URL
            if (window.location.hash && window.location.hash.length > 1) {
                try {
                    // Decode the hash
                    const hash = decodeURIComponent(window.location.hash.substring(1));
                    
                    console.log('Navigating to endpoint:', hash);
                    
                    // Split the hash to get tag and operation
                    // Format is typically: /Tag/operation_id
                    const parts = hash.split('/');
                    
                    if (parts.length >= 2) {
                        // Get the tag name (parts[1]) and operation ID (parts[2])
                        const tagName = parts[1];
                        const operationId = parts.length > 2 ? parts[2] : null;
                        
                        console.log('Looking for tag:', tagName, 'operation:', operationId);
                        
                        // Find and expand the tag
                        const tags = document.querySelectorAll('.opblock-tag');
                        for (const tag of tags) {
                            const tagText = tag.querySelector('span')?.textContent.trim();
                            
                            if (tagText && tagText === tagName) {
                                // If tag is collapsed, expand it by clicking
                                if (tag.classList.contains('is-collapsed')) {
                                    tag.click();
                                }
                                
                                // If we have an operation ID, find and expand it
                                if (operationId) {
                                    // Small delay to allow tag expansion
                                    setTimeout(function() {
                                        // Find the operation under this tag
                                        const operations = document.querySelectorAll('.opblock');
                                        
                                        for (const op of operations) {
                                            // Check if this operation matches our ID
                                            // Try different ways to match the operation
                                            const opId = op.id;
                                            const opPath = op.querySelector('.opblock-summary-path')?.textContent.trim();
                                            const opDesc = op.querySelector('.opblock-summary-description')?.textContent.trim();
                                            
                                            if ((opId && opId.includes(operationId)) || 
                                                (opDesc && opDesc.includes(operationId)) ||
                                                (opPath && operationId.includes(opPath.split('/').pop()))) {
                                                
                                                // Scroll to this operation
                                                op.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                                
                                                // If operation is collapsed, expand it
                                                if (!op.classList.contains('is-open')) {
                                                    const opSummary = op.querySelector('.opblock-summary');
                                                    if (opSummary) {
                                                        opSummary.click();
                                                    }
                                                }
                                                
                                                // Highlight this operation
                                                op.style.boxShadow = '0 0 8px #3b82f6';
                                                setTimeout(() => {
                                                    op.style.boxShadow = '';
                                                }, 2000);
                                                
                                                break;
                                            }
                                        }
                                    }, 300);
                                } else {
                                    // If no operation ID, just scroll to the tag
                                    tag.scrollIntoView({ behavior: 'smooth', block: 'start' });
                                }
                                
                                break;
                            }
                        }
                    }
                } catch (e) {
                    console.error('Error navigating to endpoint:', e);
                }
            }
        }, 500); // Give Swagger UI time to initialize
    });
    </script>
    """

    # Combine both scripts and insert them before the closing body tag
    modified_content = modified_content.replace('</body>', f'{theme_toggle_js}{hash_navigation_js}</body>')

    return HTMLResponse(content=modified_content, status_code=200)
