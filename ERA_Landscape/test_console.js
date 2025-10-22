#!/usr/bin/env node
/**
 * Autonomous console log analyzer for ERA Landscape
 * Loads page with Puppeteer, captures console, validates expected behavior
 */

const puppeteer = require('puppeteer');

async function testLandscape() {
  console.log('🚀 Starting autonomous test...\n');
  
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  const consoleLogs = [];
  const consoleWarnings = [];
  const consoleErrors = [];
  
  // Capture console messages
  page.on('console', msg => {
    const text = msg.text();
    if (msg.type() === 'error') {
      consoleErrors.push(text);
    } else if (msg.type() === 'warning') {
      consoleWarnings.push(text);
    } else {
      consoleLogs.push(text);
    }
  });
  
  // Load page
  await page.goto('http://localhost:8765', { waitUntil: 'networkidle0' });
  
  // Wait for data to load and edges to adjust (4+ seconds)
  await page.waitForTimeout(6000);
  
  // Analyze results
  console.log('📊 Console Analysis:\n');
  
  // Check for TH positioning
  const thPositioned = consoleLogs.find(log => log.includes('Fixed') && log.includes('Town Halls'));
  if (thPositioned) {
    console.log('✅ Town Halls positioned:', thPositioned);
  } else {
    console.log('❌ Town Halls NOT positioned');
  }
  
  // Check for orphan positioning
  const orphansPositioned = consoleLogs.find(log => log.includes('Positioned') && log.includes('orphan'));
  if (orphansPositioned) {
    console.log('✅ Orphans positioned:', orphansPositioned);
  } else {
    console.log('❌ Orphans NOT positioned');
  }
  
  // Check for edge adjustments
  const edgeAdjustment = consoleLogs.find(log => log.includes('Adjusted') && log.includes('TH→person'));
  if (edgeAdjustment) {
    console.log('✅ Edges adjusted:', edgeAdjustment);
    
    // Parse near/medium/far counts
    const match = edgeAdjustment.match(/(\d+) near.*?(\d+) medium.*?(\d+) far/);
    if (match) {
      const [, near, medium, far] = match;
      console.log(`   📈 Distribution: ${near} near, ${medium} medium, ${far} far`);
      
      if (parseInt(near) === 0) {
        console.log('   ⚠️  WARNING: No near edges! Orphans may still be too far.');
      } else {
        console.log(`   ✅ SUCCESS: ${near} thick edges should be visible!`);
      }
    }
  } else {
    console.log('❌ Edge adjustment NOT found');
  }
  
  // Check for warnings
  if (consoleWarnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    consoleWarnings.forEach(w => console.log('   -', w));
  }
  
  // Check for errors
  if (consoleErrors.length > 0) {
    console.log('\n❌ Errors:');
    consoleErrors.forEach(e => console.log('   -', e));
  }
  
  await browser.close();
  
  console.log('\n✨ Test complete');
}

testLandscape().catch(console.error);
