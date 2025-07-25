// This file contains utility functions for testing the website on different devices and browsers

/**
 * Responsive breakpoints for testing
 */
export const breakpoints = {
  mobile: {
    width: 375,
    height: 667,
    name: 'Mobile (iPhone SE)'
  },
  tablet: {
    width: 768,
    height: 1024,
    name: 'Tablet (iPad)'
  },
  laptop: {
    width: 1366,
    height: 768,
    name: 'Laptop'
  },
  desktop: {
    width: 1920,
    height: 1080,
    name: 'Desktop'
  }
};

/**
 * Test cases for validation
 */
export const testCases = [
  {
    name: 'Homepage Rendering',
    description: 'Verify that the homepage renders correctly on all devices',
    steps: [
      'Navigate to the homepage',
      'Check that all sections are visible',
      'Verify that buttons and links are clickable',
      'Ensure images load properly'
    ]
  },
  {
    name: 'Machine Locator Functionality',
    description: 'Test the machine locator for both donors and receivers',
    steps: [
      'Navigate to the machine locator page',
      'Switch between donor and receiver views',
      'Verify that maps and machine listings display correctly',
      'Test filtering and sorting options'
    ]
  },
  {
    name: 'Admin Authentication',
    description: 'Verify admin login and dashboard access',
    steps: [
      'Navigate to the admin login page',
      'Test login with valid credentials',
      'Test login with invalid credentials',
      'Verify redirect to dashboard after successful login',
      'Check that protected routes require authentication'
    ]
  },
  {
    name: 'Volunteer Authentication',
    description: 'Verify volunteer login and portal access',
    steps: [
      'Navigate to the volunteer login page',
      'Test login with valid credentials',
      'Test login with invalid credentials',
      'Verify redirect to portal after successful login',
      'Check that protected routes require authentication'
    ]
  },
  {
    name: 'Admin Dashboard Functionality',
    description: 'Test all features of the admin dashboard',
    steps: [
      'Login as admin',
      'Verify that all statistics display correctly',
      'Test machine management features',
      'Test volunteer management features',
      'Verify that alerts display correctly'
    ]
  },
  {
    name: 'Volunteer Portal Functionality',
    description: 'Test all features of the volunteer portal',
    steps: [
      'Login as volunteer',
      'Verify that assigned machines display correctly',
      'Test task management features',
      'Check activity log functionality',
      'Verify that alerts display correctly'
    ]
  },
  {
    name: 'Responsive Design',
    description: 'Verify that the website is responsive on all devices',
    steps: [
      'Test all pages on mobile, tablet, laptop, and desktop',
      'Verify that layouts adjust appropriately',
      'Check that text is readable on all devices',
      'Ensure that touch targets are appropriate for mobile'
    ]
  },
  {
    name: 'Accessibility',
    description: 'Verify that the website is accessible',
    steps: [
      'Test keyboard navigation',
      'Verify that all images have alt text',
      'Check color contrast for readability',
      'Ensure that form inputs have labels'
    ]
  },
  {
    name: 'Error Handling',
    description: 'Test error handling throughout the application',
    steps: [
      'Test form validation',
      'Verify that API errors display appropriate messages',
      'Check that network errors are handled gracefully',
      'Test authentication errors'
    ]
  },
  {
    name: 'Performance',
    description: 'Verify that the website performs well',
    steps: [
      'Check page load times',
      'Verify that animations are smooth',
      'Test performance on lower-end devices',
      'Ensure that API calls are optimized'
    ]
  }
];

/**
 * Generate a test report
 * @param results Array of test results
 * @returns Formatted test report
 */
export function generateTestReport(results) {
  const totalTests = results.length;
  const passedTests = results.filter(r => r.passed).length;
  const failedTests = totalTests - passedTests;
  
  let report = `# Website Testing Report\n\n`;
  report += `**Date:** ${new Date().toLocaleDateString()}\n`;
  report += `**Summary:** ${passedTests}/${totalTests} tests passed (${Math.round(passedTests/totalTests*100)}%)\n\n`;
  
  report += `## Test Results\n\n`;
  
  results.forEach(result => {
    report += `### ${result.name}\n`;
    report += `**Status:** ${result.passed ? '✅ PASSED' : '❌ FAILED'}\n`;
    report += `**Description:** ${result.description}\n`;
    
    if (result.notes) {
      report += `**Notes:** ${result.notes}\n`;
    }
    
    if (result.issues && result.issues.length > 0) {
      report += `**Issues:**\n`;
      result.issues.forEach(issue => {
        report += `- ${issue}\n`;
      });
    }
    
    report += `\n`;
  });
  
  return report;
}
