import { useEffect, useRef, useCallback } from 'react';

interface PerformanceMetrics {
  loadTime: number;
  renderTime: number;
  memoryUsage?: number;
  networkRequests: number;
  errors: number;
}

interface PerformanceOptions {
  trackMemory?: boolean;
  trackNetwork?: boolean;
  trackErrors?: boolean;
  sampleRate?: number; // 0-1, percentage of sessions to track
}

export function usePerformance(
  componentName: string,
  options: PerformanceOptions = {}
) {
  const {
    trackMemory = false,
    trackNetwork = true,
    trackErrors = true,
    sampleRate = 1.0
  } = options;

  const startTime = useRef<number>(Date.now());
  const renderStartTime = useRef<number>(0);
  const metrics = useRef<PerformanceMetrics>({
    loadTime: 0,
    renderTime: 0,
    memoryUsage: 0,
    networkRequests: 0,
    errors: 0
  });

  // Check if we should track this session
  const shouldTrack = Math.random() < sampleRate;

  // Track component mount time
  useEffect(() => {
    if (!shouldTrack) return;

    const mountTime = Date.now();
    metrics.current.loadTime = mountTime - startTime.current;

    // Track memory usage if enabled
    if (trackMemory && 'memory' in performance) {
      const memory = (performance as any).memory;
      if (memory) {
        metrics.current.memoryUsage = memory.usedJSHeapSize / 1024 / 1024; // MB
      }
    }

    // Log performance metrics
    console.log(`[Performance] ${componentName} mounted:`, {
      loadTime: metrics.current.loadTime,
      memoryUsage: metrics.current.memoryUsage
    });

    // Send metrics to analytics service in production
    if (process.env.NODE_ENV === 'production') {
      sendMetricsToAnalytics(componentName, metrics.current);
    }
  }, [componentName, trackMemory, shouldTrack]);

  // Track render performance
  const trackRender = useCallback(() => {
    if (!shouldTrack) return;

    renderStartTime.current = performance.now();
  }, [shouldTrack]);

  const endRender = useCallback(() => {
    if (!shouldTrack || renderStartTime.current === 0) return;

    const renderTime = performance.now() - renderStartTime.current;
    metrics.current.renderTime = renderTime;

    // Log slow renders
    if (renderTime > 16) { // More than one frame at 60fps
      console.warn(`[Performance] Slow render in ${componentName}:`, renderTime);
    }
  }, [componentName, shouldTrack]);

  // Track network requests
  const trackNetworkRequest = useCallback(() => {
    if (!shouldTrack || !trackNetwork) return;

    metrics.current.networkRequests += 1;
  }, [shouldTrack, trackNetwork]);

  // Track errors
  const trackError = useCallback((error: Error) => {
    if (!shouldTrack || !trackErrors) return;

    metrics.current.errors += 1;
    console.error(`[Performance] Error in ${componentName}:`, error);
  }, [componentName, shouldTrack, trackErrors]);

  // Track user interactions
  const trackInteraction = useCallback((action: string, data?: any) => {
    if (!shouldTrack) return;

    console.log(`[Performance] ${componentName} interaction:`, { action, data });
  }, [componentName, shouldTrack]);

  // Track page visibility changes
  useEffect(() => {
    if (!shouldTrack) return;

    const handleVisibilityChange = () => {
      if (document.hidden) {
        console.log(`[Performance] ${componentName} became hidden`);
      } else {
        console.log(`[Performance] ${componentName} became visible`);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [componentName, shouldTrack]);

  // Track memory usage periodically
  useEffect(() => {
    if (!shouldTrack || !trackMemory) return;

    const interval = setInterval(() => {
      if ('memory' in performance) {
        const memory = (performance as any).memory;
        if (memory) {
          const currentMemory = memory.usedJSHeapSize / 1024 / 1024;
          if (currentMemory > metrics.current.memoryUsage!) {
            metrics.current.memoryUsage = currentMemory;
          }
        }
      }
    }, 5000); // Check every 5 seconds

    return () => clearInterval(interval);
  }, [trackMemory, shouldTrack]);

  return {
    trackRender,
    endRender,
    trackNetworkRequest,
    trackError,
    trackInteraction,
    metrics: metrics.current
  };
}

// Send metrics to analytics service
function sendMetricsToAnalytics(componentName: string, metrics: PerformanceMetrics) {
  // In a real application, you would send this to your analytics service
  // For example: Google Analytics, Mixpanel, or a custom analytics endpoint
  
  const analyticsData = {
    component: componentName,
    timestamp: Date.now(),
    metrics: {
      loadTime: metrics.loadTime,
      renderTime: metrics.renderTime,
      memoryUsage: metrics.memoryUsage,
      networkRequests: metrics.networkRequests,
      errors: metrics.errors
    },
    userAgent: navigator.userAgent,
    url: window.location.href
  };

  // Example: Send to custom analytics endpoint
  // fetch('/api/analytics/performance', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(analyticsData)
  // }).catch(console.error);

  console.log('[Analytics] Performance metrics:', analyticsData);
}

// Hook for tracking page performance
export function usePagePerformance(pageName: string) {
  const performance = usePerformance(pageName, {
    trackMemory: true,
    trackNetwork: true,
    trackErrors: true,
    sampleRate: 0.1 // Track 10% of page loads
  });

  // Track page load time
  useEffect(() => {
    const handleLoad = () => {
      const loadTime = performance.now();
      console.log(`[Performance] Page ${pageName} loaded in ${loadTime}ms`);
    };

    if (document.readyState === 'complete') {
      handleLoad();
    } else {
      window.addEventListener('load', handleLoad);
      return () => window.removeEventListener('load', handleLoad);
    }
  }, [pageName]);

  return performance;
}

// Hook for tracking component performance
export function useComponentPerformance(componentName: string) {
  return usePerformance(componentName, {
    trackMemory: false,
    trackNetwork: false,
    trackErrors: true,
    sampleRate: 0.05 // Track 5% of component renders
  });
}
