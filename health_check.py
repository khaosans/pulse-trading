"""
Health Check & System Monitoring Module
Monitors application health and provides diagnostic information
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import platform
import streamlit as st
import psutil
import time


class HealthStatus:
    """Health status constants"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheck:
    """Application health monitoring"""
    
    @staticmethod
    def check_dependencies() -> Dict[str, Any]:
        """
        Check if all required dependencies are available
        
        Returns:
            dict: Dependency status
        """
        dependencies = {
            'streamlit': False,
            'pandas': False,
            'numpy': False,
            'plotly': False,
            'requests': False,
            'yfinance': False,
        }
        
        results = {}
        
        for dep in dependencies:
            try:
                __import__(dep)
                results[dep] = {
                    'status': HealthStatus.HEALTHY,
                    'available': True,
                    'version': __import__(dep).__version__ if hasattr(__import__(dep), '__version__') else 'unknown'
                }
            except ImportError:
                results[dep] = {
                    'status': HealthStatus.UNHEALTHY,
                    'available': False,
                    'error': f'{dep} not installed'
                }
        
        return results
    
    @staticmethod
    def check_custom_modules() -> Dict[str, Any]:
        """
        Check if custom modules are available
        
        Returns:
            dict: Module status
        """
        modules = [
            'app_enhancements',
            'ui_components',
            'performance_config',
            'live_data',
            'validation',
        ]
        
        results = {}
        
        for module in modules:
            try:
                __import__(module)
                results[module] = {
                    'status': HealthStatus.HEALTHY,
                    'available': True
                }
            except ImportError as e:
                results[module] = {
                    'status': HealthStatus.DEGRADED,
                    'available': False,
                    'error': str(e)
                }
        
        return results
    
    @staticmethod
    def check_system_resources() -> Dict[str, Any]:
        """
        Check system resource usage
        
        Returns:
            dict: Resource usage information
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Determine health status
            cpu_status = HealthStatus.HEALTHY
            if cpu_percent > 80:
                cpu_status = HealthStatus.DEGRADED
            if cpu_percent > 95:
                cpu_status = HealthStatus.UNHEALTHY
            
            memory_status = HealthStatus.HEALTHY
            if memory.percent > 80:
                memory_status = HealthStatus.DEGRADED
            if memory.percent > 95:
                memory_status = HealthStatus.UNHEALTHY
            
            disk_status = HealthStatus.HEALTHY
            if disk.percent > 85:
                disk_status = HealthStatus.DEGRADED
            if disk.percent > 95:
                disk_status = HealthStatus.UNHEALTHY
            
            return {
                'cpu': {
                    'status': cpu_status,
                    'usage_percent': cpu_percent,
                    'cores': psutil.cpu_count()
                },
                'memory': {
                    'status': memory_status,
                    'usage_percent': memory.percent,
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2)
                },
                'disk': {
                    'status': disk_status,
                    'usage_percent': disk.percent,
                    'total_gb': round(disk.total / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2)
                }
            }
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'error': f'Failed to get system resources: {str(e)}'
            }
    
    @staticmethod
    def check_cache_health() -> Dict[str, Any]:
        """
        Check cache system health
        
        Returns:
            dict: Cache status
        """
        try:
            # Check if Streamlit cache is working
            cache_status = HealthStatus.HEALTHY
            
            # Simple cache test
            @st.cache_data(ttl=1)
            def cache_test():
                return time.time()
            
            first_call = cache_test()
            second_call = cache_test()
            
            if first_call == second_call:
                cache_working = True
            else:
                cache_working = False
                cache_status = HealthStatus.DEGRADED
            
            return {
                'status': cache_status,
                'working': cache_working,
                'message': 'Cache is functioning' if cache_working else 'Cache may have issues'
            }
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'working': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            dict: System details
        """
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': sys.version.split()[0],
            'streamlit_version': st.__version__,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def run_full_health_check() -> Dict[str, Any]:
        """
        Run complete health check
        
        Returns:
            dict: Complete health status
        """
        start_time = time.time()
        
        dependencies = HealthCheck.check_dependencies()
        custom_modules = HealthCheck.check_custom_modules()
        resources = HealthCheck.check_system_resources()
        cache = HealthCheck.check_cache_health()
        system_info = HealthCheck.get_system_info()
        
        # Determine overall health
        all_checks = []
        
        # Check dependencies
        for dep in dependencies.values():
            if dep.get('status') == HealthStatus.UNHEALTHY:
                all_checks.append(HealthStatus.UNHEALTHY)
            elif dep.get('status') == HealthStatus.DEGRADED:
                all_checks.append(HealthStatus.DEGRADED)
            else:
                all_checks.append(HealthStatus.HEALTHY)
        
        # Check resources
        if isinstance(resources, dict) and 'status' not in resources:
            all_checks.extend([
                resources['cpu']['status'],
                resources['memory']['status'],
                resources['disk']['status']
            ])
        
        # Check cache
        all_checks.append(cache['status'])
        
        # Determine overall status
        if HealthStatus.UNHEALTHY in all_checks:
            overall_status = HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in all_checks:
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.HEALTHY
        
        elapsed_time = time.time() - start_time
        
        return {
            'overall_status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'check_duration_ms': round(elapsed_time * 1000, 2),
            'dependencies': dependencies,
            'custom_modules': custom_modules,
            'system_resources': resources,
            'cache_health': cache,
            'system_info': system_info
        }


class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation: str) -> None:
        """
        Start timing an operation
        
        Args:
            operation: Operation name
        """
        self.start_times[operation] = time.time()
    
    def stop_timer(self, operation: str) -> Optional[float]:
        """
        Stop timing an operation
        
        Args:
            operation: Operation name
            
        Returns:
            float: Elapsed time in seconds, or None if not started
        """
        if operation not in self.start_times:
            return None
        
        elapsed = time.time() - self.start_times[operation]
        
        if operation not in self.metrics:
            self.metrics[operation] = []
        
        self.metrics[operation].append(elapsed)
        del self.start_times[operation]
        
        return elapsed
    
    def get_stats(self, operation: str) -> Optional[Dict[str, float]]:
        """
        Get statistics for an operation
        
        Args:
            operation: Operation name
            
        Returns:
            dict: Statistics including min, max, avg, count
        """
        if operation not in self.metrics or not self.metrics[operation]:
            return None
        
        times = self.metrics[operation]
        
        return {
            'count': len(times),
            'min_ms': round(min(times) * 1000, 2),
            'max_ms': round(max(times) * 1000, 2),
            'avg_ms': round(sum(times) / len(times) * 1000, 2),
            'total_ms': round(sum(times) * 1000, 2)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """
        Get statistics for all operations
        
        Returns:
            dict: All operation statistics
        """
        return {
            operation: self.get_stats(operation)
            for operation in self.metrics.keys()
        }
    
    def reset(self) -> None:
        """Reset all metrics"""
        self.metrics = {}
        self.start_times = {}


def render_health_dashboard():
    """
    Render health check dashboard in Streamlit
    """
    st.markdown("### 🏥 System Health Dashboard")
    
    with st.spinner("Running health checks..."):
        health_data = HealthCheck.run_full_health_check()
    
    # Overall status
    status = health_data['overall_status']
    status_icon = {
        HealthStatus.HEALTHY: "✅",
        HealthStatus.DEGRADED: "⚠️",
        HealthStatus.UNHEALTHY: "❌"
    }
    
    status_color = {
        HealthStatus.HEALTHY: "green",
        HealthStatus.DEGRADED: "orange",
        HealthStatus.UNHEALTHY: "red"
    }
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(29, 111, 122, 0.1) 0%, rgba(42, 165, 179, 0.1) 100%);
                padding: 2rem; border-radius: 12px; text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{status_icon[status]}</div>
        <h2 style="color: {status_color[status]}; margin: 0;">System Status: {status.upper()}</h2>
        <p style="color: #4A5568; margin-top: 0.5rem;">
            Health check completed in {health_data['check_duration_ms']}ms
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Dependencies")
        for dep, info in health_data['dependencies'].items():
            status_icon = "✅" if info['available'] else "❌"
            version = info.get('version', 'N/A')
            st.markdown(f"{status_icon} **{dep}** - v{version}")
        
        st.markdown("---")
        
        st.markdown("#### 🧩 Custom Modules")
        for module, info in health_data['custom_modules'].items():
            status_icon = "✅" if info['available'] else "⚠️"
            st.markdown(f"{status_icon} **{module}**")
    
    with col2:
        st.markdown("#### 💻 System Resources")
        resources = health_data['system_resources']
        
        if 'cpu' in resources:
            st.metric(
                "CPU Usage",
                f"{resources['cpu']['usage_percent']:.1f}%",
                delta=None,
                delta_color="off"
            )
            
            st.metric(
                "Memory Usage",
                f"{resources['memory']['usage_percent']:.1f}%",
                delta=f"{resources['memory']['available_gb']:.1f}GB free"
            )
            
            st.metric(
                "Disk Usage",
                f"{resources['disk']['usage_percent']:.1f}%",
                delta=f"{resources['disk']['free_gb']:.1f}GB free"
            )
    
    # Cache health
    cache_status = health_data['cache_health']
    cache_icon = "✅" if cache_status['working'] else "❌"
    st.markdown(f"#### 💾 Cache Status: {cache_icon} {cache_status['message']}")
    
    # System info
    with st.expander("🖥️ System Information"):
        info = health_data['system_info']
        st.json(info)
    
    # Raw data
    with st.expander("📊 Raw Health Data"):
        st.json(health_data)


# Export commonly used classes
__all__ = [
    'HealthStatus',
    'HealthCheck',
    'PerformanceMonitor',
    'render_health_dashboard',
]

