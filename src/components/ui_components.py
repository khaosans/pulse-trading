"""
Reusable UI Components for PulseTrade
Ensures consistency and reduces code duplication
"""

import streamlit as st
from typing import Optional, Dict, Any, List
import plotly.graph_objects as go
from datetime import datetime

def render_loading_state(message: str = "Loading...", key: Optional[str] = None):
    """
    Consistent loading state component
    
    Args:
        message: Loading message to display
        key: Unique key for the component
    """
    st.markdown(f"""
    <div class="loading-container" style="text-align: center; padding: 2rem;">
        <div class="spinner" style="margin: 0 auto; border: 3px solid rgba(29, 111, 122, 0.1);
                    border-top-color: #1D6F7A; border-radius: 50%; width: 40px; height: 40px;
                    animation: spin 1s linear infinite;"></div>
        <p style="margin-top: 1rem; color: #4A5568;">{message}</p>
    </div>
    
    <style>
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
    """, unsafe_allow_html=True)


def render_error_state(error_message: str, retry_callback=None):
    """
    Consistent error state component
    
    Args:
        error_message: Error message to display
        retry_callback: Optional function to call on retry
    """
    st.error(f"""
    **Error Occurred**
    
    {error_message}
    
    Please try again or contact support if the issue persists.
    """)
    
    if retry_callback:
        if st.button("🔄 Retry", key=f"retry_{hash(error_message)}"):
            retry_callback()


def render_metric_card(label: str, value: str, delta: Optional[str] = None, 
                       delta_color: str = "normal", icon: str = "📊"):
    """
    Consistent metric card component
    
    Args:
        label: Metric label
        value: Metric value
        delta: Change value (optional)
        delta_color: Color for delta (normal, inverse, off)
        icon: Emoji icon
    """
    delta_html = ""
    if delta:
        color = "#10B981" if delta_color == "normal" and delta.startswith("+") else "#EF4444"
        delta_html = f'<div style="color: {color}; font-weight: 700; font-size: 1rem; margin-top: 0.5rem;">{delta}</div>'
    
    st.markdown(f"""
    <div class="metric-card card" style="text-align: center; padding: 1.5rem; animation: fadeIn 0.3s;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-label" style="color: #718096; font-size: 0.875rem; font-weight: 700; 
                    text-transform: uppercase; margin-bottom: 0.5rem;">
            {label}
        </div>
        <div class="metric-value" style="font-size: 2rem; font-weight: 800; color: #1D6F7A;">
            {value}
        </div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_status_badge(label: str, status: str = "success"):
    """
    Consistent status badge component
    
    Args:
        label: Badge text
        status: Badge status (success, warning, error, info)
    """
    colors = {
        "success": {"bg": "#D1FAE5", "text": "#065F46", "border": "#10B981"},
        "warning": {"bg": "#FEF3C7", "text": "#92400E", "border": "#F59E0B"},
        "error": {"bg": "#FEE2E2", "text": "#991B1B", "border": "#EF4444"},
        "info": {"bg": "#DBEAFE", "text": "#1E40AF", "border": "#3B82F6"},
    }
    
    color = colors.get(status, colors["info"])
    
    return f"""
    <span style="background: {color['bg']}; color: {color['text']}; 
                 padding: 0.35rem 0.85rem; border-radius: 14px; font-size: 0.75rem;
                 font-weight: 700; display: inline-block; border: 2px solid {color['border']};
                 text-transform: uppercase; letter-spacing: 0.5px;">
        {label}
    </span>
    """


def render_empty_state(message: str, icon: str = "📭", action_text: Optional[str] = None, 
                       action_callback=None):
    """
    Consistent empty state component
    
    Args:
        message: Empty state message
        icon: Emoji icon
        action_text: Optional action button text
        action_callback: Optional action callback
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem; color: #718096;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_text and action_callback:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(action_text, type="primary", use_container_width=True):
                action_callback()


def render_info_card(title: str, content: str, type: str = "info"):
    """
    Consistent info/alert card component
    
    Args:
        title: Card title
        content: Card content
        type: Card type (info, success, warning, error)
    """
    colors = {
        "info": {"bg": "rgba(59, 130, 246, 0.1)", "border": "#3B82F6", "icon": "ℹ️"},
        "success": {"bg": "rgba(16, 185, 129, 0.1)", "border": "#10B981", "icon": "✅"},
        "warning": {"bg": "rgba(245, 158, 11, 0.1)", "border": "#F59E0B", "icon": "⚠️"},
        "error": {"bg": "rgba(239, 68, 68, 0.1)", "border": "#EF4444", "icon": "❌"},
    }
    
    color = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div style="background: {color['bg']}; padding: 1.5rem; border-radius: 12px; 
                margin: 1rem 0; border-left: 4px solid {color['border']};">
        <h4 style="color: #1D6F7A; margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
            <span>{color['icon']}</span>
            <span>{title}</span>
        </h4>
        <p style="color: #4A5568; margin-bottom: 0; line-height: 1.6;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """
    Consistent section header component
    
    Args:
        title: Section title
        subtitle: Optional subtitle
        icon: Optional emoji icon
    """
    icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''
    subtitle_html = f'<p style="color: #718096; font-size: 1rem; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="section-header" style="margin-bottom: 2rem;">
        <h2 style="color: #1D6F7A; font-weight: 700; font-size: 2rem; margin-bottom: 0.5rem;">
            {icon_html}{title}
        </h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def render_data_table(data, title: Optional[str] = None, max_rows: int = 100):
    """
    Optimized data table component
    
    Args:
        data: DataFrame to display
        title: Optional table title
        max_rows: Maximum rows to display for performance
    """
    if title:
        st.markdown(f"### {title}")
    
    if data is None or len(data) == 0:
        render_empty_state("No data available", "📊")
        return
    
    # Optimize large datasets
    if len(data) > max_rows:
        st.info(f"Showing {max_rows} of {len(data)} rows for performance")
        data = data.head(max_rows)
    
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
    )


def create_consistent_chart(df, chart_type: str = "line", **kwargs):
    """
    Create chart with consistent styling
    
    Args:
        df: Data for the chart
        chart_type: Type of chart (line, bar, candlestick, pie)
        **kwargs: Additional chart arguments
    """
    fig = go.Figure()
    
    # Consistent layout settings
    layout_settings = {
        'template': 'plotly_white',
        'font': {'size': 12, 'color': '#4A5568', 'family': 'Arial, sans-serif'},
        'plot_bgcolor': '#F8F9FA',
        'paper_bgcolor': '#FFFFFF',
        'hovermode': 'x unified',
        'margin': {'t': 60, 'b': 40, 'l': 40, 'r': 40},
    }
    
    fig.update_layout(**layout_settings)
    
    return fig


def render_accessibility_skip_link():
    """
    Add skip to main content link for accessibility
    """
    st.markdown("""
    <a href="#main-content" class="skip-to-main" 
       style="position: absolute; top: -40px; left: 0; background: #1D6F7A; 
              color: white; padding: 8px; text-decoration: none; z-index: 100;">
        Skip to main content
    </a>
    
    <style>
    .skip-to-main:focus {
        top: 0;
    }
    </style>
    
    <div id="main-content"></div>
    """, unsafe_allow_html=True)


def with_error_boundary(func, fallback_message: str = "An error occurred"):
    """
    Decorator for error boundaries
    
    Args:
        func: Function to wrap
        fallback_message: Message to show on error
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            render_error_state(f"{fallback_message}: {str(e)}")
            st.exception(e)  # Show full error in debug mode
    
    return wrapper


# Consistent color palette for charts
CHART_COLORS = {
    'primary': '#1D6F7A',
    'primary_light': '#2AA5B3', 
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
    'neutral': '#6B7280',
}

# Responsive column layouts
def get_responsive_columns(mobile: int = 1, tablet: int = 2, desktop: int = 3):
    """
    Get responsive column layout based on viewport
    
    Args:
        mobile: Columns for mobile
        tablet: Columns for tablet  
        desktop: Columns for desktop
        
    Returns:
        Column layout
    """
    # Streamlit doesn't have viewport detection, so we use desktop by default
    # but this provides a consistent API for future enhancement
    return st.columns(desktop)


# ============================================
# BANKING & FREELANCER UI COMPONENTS (NEW)
# ============================================

def render_account_card(account_data: Dict[str, Any]):
    """
    Render bank account card with balance and details
    
    Args:
        account_data: Account information
    """
    balance = account_data.get('balance', 0)
    available = account_data.get('available_balance', 0)
    account_type = account_data.get('account_type', 'checking').title()
    
    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg, #1D6F7A 0%, #2AA5B3 100%); 
                color: white; padding: 2rem; border-radius: 16px; margin: 1rem 0;">
        <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.5rem;">
            {account_type} Account
        </div>
        <div style="font-size: 2.5rem; font-weight: 800; margin: 1rem 0;">
            ${balance:,.2f}
        </div>
        <div style="font-size: 0.875rem; opacity: 0.9;">
            Available: ${available:,.2f}
        </div>
        <div style="margin-top: 1.5rem; font-size: 0.75rem; opacity: 0.8;">
            ••••  {account_data.get('account_number', '0000')[-4:]}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_invoice_card(invoice: Dict[str, Any]):
    """
    Render invoice card with status and details
    
    Args:
        invoice: Invoice data
    """
    status = invoice.get('status', 'draft')
    status_colors = {
        'draft': {'bg': '#F3F4F6', 'text': '#374151'},
        'sent': {'bg': '#DBEAFE', 'text': '#1E40AF'},
        'viewed': {'bg': '#FEF3C7', 'text': '#92400E'},
        'paid': {'bg': '#D1FAE5', 'text': '#065F46'},
        'overdue': {'bg': '#FEE2E2', 'text': '#991B1B'}
    }
    
    color = status_colors.get(status, status_colors['draft'])
    
    st.markdown(f"""
    <div class="card" style="padding: 1.5rem; margin: 0.75rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #1A202C;">
                    {invoice.get('invoice_number', 'INV-0000')}
                </div>
                <div style="color: #718096; font-size: 0.875rem; margin-top: 0.25rem;">
                    {invoice.get('client_name', 'Client')}
                </div>
            </div>
            <div style="background: {color['bg']}; color: {color['text']}; 
                        padding: 0.5rem 1rem; border-radius: 24px; font-weight: 600; font-size: 0.875rem;">
                {status.upper()}
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #1D6F7A; font-size: 1.75rem; font-weight: 800;">
                    ${invoice.get('total_amount', 0):,.2f}
                </div>
            </div>
            <div style="text-align: right; color: #718096; font-size: 0.875rem;">
                Due: {invoice.get('due_date', datetime.now()).strftime('%b %d, %Y') if isinstance(invoice.get('due_date'), datetime) else 'N/A'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_payment_status(payment: Dict[str, Any]):
    """
    Render payment status with timeline
    
    Args:
        payment: Payment details
    """
    status = payment.get('status', 'pending')
    status_info = {
        'pending': {'icon': '⏳', 'color': '#F59E0B', 'label': 'Pending'},
        'processing': {'icon': '🔄', 'color': '#3B82F6', 'label': 'Processing'},
        'completed': {'icon': '✅', 'color': '#10B981', 'label': 'Completed'},
        'failed': {'icon': '❌', 'color': '#EF4444', 'label': 'Failed'}
    }
    
    info = status_info.get(status, status_info['pending'])
    
    st.markdown(f"""
    <div class="card" style="padding: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">{info['icon']}</div>
            <div>
                <div style="font-weight: 700; font-size: 1.1rem; color: {info['color']};">
                    {info['label']}
                </div>
                <div style="color: #718096; font-size: 0.875rem;">
                    ${payment.get('amount', 0):,.2f}
                </div>
            </div>
        </div>
        <div style="color: #4A5568; font-size: 0.875rem;">
            {payment.get('description', 'Payment')}
        </div>
        {f'<div style="color: #718096; font-size: 0.75rem; margin-top: 0.5rem;">Expected: {payment.get("expected_completion").strftime("%b %d, %Y") if payment.get("expected_completion") else "N/A"}</div>' if payment.get('expected_completion') else ''}
    </div>
    """, unsafe_allow_html=True)


def render_tax_savings_widget(tax_data: Dict[str, Any]):
    """
    Render tax savings status widget
    
    Args:
        tax_data: Tax savings data
    """
    saved = tax_data.get('saved', 0)
    recommended = tax_data.get('recommended', 0)
    percentage = (saved / recommended * 100) if recommended > 0 else 0
    
    if percentage >= 100:
        color = '#10B981'
        status = '✅ On Track'
    elif percentage >= 80:
        color = '#F59E0B'
        status = '⚠️ Nearly There'
    else:
        color = '#EF4444'
        status = '🚨 Behind'
    
    st.markdown(f"""
    <div class="card" style="padding: 1.5rem; background: linear-gradient(135deg, rgba(29, 111, 122, 0.05) 0%, rgba(42, 165, 179, 0.05) 100%);">
        <div style="font-weight: 700; font-size: 1.1rem; color: {color}; margin-bottom: 1rem;">
            {status}
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #718096;">Saved for Taxes</span>
            <span style="font-weight: 700; color: #1D6F7A;">${saved:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <span style="color: #718096;">Recommended</span>
            <span style="color: #718096;">${recommended:,.0f}</span>
        </div>
        <div style="background: #E5E7EB; height: 8px; border-radius: 4px; overflow: hidden;">
            <div style="background: {color}; height: 100%; width: {min(100, percentage)}%; 
                        transition: width 0.3s ease;"></div>
        </div>
        <div style="text-align: center; margin-top: 0.5rem; color: #718096; font-size: 0.875rem;">
            {percentage:.0f}% of recommended savings
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_cash_flow_forecast(forecast_data: Dict[str, Any]):
    """
    Render cash flow forecast chart
    
    Args:
        forecast_data: Forecast data with dates and values
    """
    import plotly.graph_objects as go
    
    df = forecast_data.get('forecast')
    
    if df is None or df.empty:
        render_empty_state("No forecast data available", "📈")
        return
    
    fig = go.Figure()
    
    # Add confidence band
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['confidence_high'],
        fill=None,
        mode='lines',
        line=dict(color='rgba(29, 111, 122, 0.2)', width=0),
        showlegend=False,
        name='Upper Bound'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['confidence_low'],
        fill='tonexty',
        mode='lines',
        line=dict(color='rgba(29, 111, 122, 0.2)', width=0),
        fillcolor='rgba(29, 111, 122, 0.2)',
        name='Confidence Band'
    ))
    
    # Add actual forecast
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['cumulative_cash_flow'],
        mode='lines',
        line=dict(color='#1D6F7A', width=3),
        name='Forecast'
    ))
    
    fig.update_layout(
        title='Cash Flow Forecast',
        xaxis_title='Date',
        yaxis_title='Cash Flow ($)',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_expense_category_chart(expense_data: Dict[str, float]):
    """
    Render expense breakdown by category
    
    Args:
        expense_data: Category -> Amount mapping
    """
    import plotly.express as px
    
    if not expense_data:
        render_empty_state("No expense data", "📊")
        return
    
    fig = px.pie(
        names=list(expense_data.keys()),
        values=list(expense_data.values()),
        title='Expense Breakdown',
        color_discrete_sequence=px.colors.sequential.Teal
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)


def render_quick_action_button(label: str, icon: str, description: str, key: str):
    """
    Render quick action button
    
    Args:
        label: Button label
        icon: Emoji icon
        description: Button description
        key: Unique key
    """
    button_clicked = st.button(
        f"{icon} {label}",
        key=key,
        use_container_width=True,
        help=description
    )
    
    return button_clicked

