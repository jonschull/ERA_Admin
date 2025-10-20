# Goals and Success Criteria for Fathom HTML-to-Markdown Conversion

## 1. Primary Goal

The primary goal is to convert the HTML body of Fathom meeting summary emails into a clean, well-structured, and human-readable Markdown format. This process must reliably extract all meaningful content and metadata while discarding irrelevant HTML styling and scripts. The final output should preserve the logical hierarchy and all embedded hyperlinks from the original email.

---

## 2. Desired Output Structure

The converted Markdown file must follow this exact structure, based on the visual layout of the original Fathom email:

1.  **Subtitle:** A subtitle indicating the Fathom account owner (e.g., *Meeting with Enabling The Future*).
2.  **Main Title (H1):** The primary meeting title, which includes the main participant and their organization (e.g., `# Gwynant from Restor.eco`).
3.  **Metadata Line:** A single line containing the meeting date, duration, and the "View Meeting" and "Ask Fathom" hyperlinks.
4.  **Action Items (H2):** The "ACTION ITEMS" section, placed immediately after the header.
5.  **Meeting Purpose (H2):** The purpose of the meeting.
6.  **Key Takeaways (H2):** A bulleted list of key takeaways.
7.  **Topics (H2):** The main topics section, containing nested subsections.
    - **Subsections (H3):** All subsections like "Restor.eco Overview" or "Data Sharing Opportunities" must be included as H3 headings.
8.  **Next Steps (H2):** If present, the "Next Steps" section.

---

## 3. Success Criteria Checklist

For a conversion to be considered successful, it must meet all of the following criteria:

- [ ] **No Data Loss:** All textual content from the original meeting summary must be present in the final Markdown.
- [ ] **Correct Header Extraction:**
    - [ ] The main participant and organization are correctly identified and formatted as the `#` Main Title.
    - [ ] The meeting date and duration are correctly extracted and displayed.
- [ ] **Action Items at the Top:**
    - [ ] The "ACTION ITEMS" section is correctly identified and placed immediately after the header information.
    - [ ] Each action item is formatted as a Markdown checkbox (`- [ ]`).
    - [ ] The assignee (e.g., *Jon Schull*) is correctly associated with its action item.
- [ ] **Preservation of All Hyperlinks:**
    - [ ] **Crucially, all hyperlinks to Fathom recording timestamps must be preserved.** This applies to:
        - Action Items
        - Key Takeaways
        - All bullet points within all "Topics" subsections
        - Next Steps
- [ ] **Correct Structural Hierarchy:**
    - [ ] Major sections ("Meeting Purpose", "Key Takeaways", etc.) are correctly identified and formatted as `##` headings.
    - [ ] All subsections within "Topics" are correctly identified and formatted as `###` headings.
- [ ] **Clean and Readable Output:**
    - [ ] The final Markdown is free of all HTML tags (e.g., `<div>`, `<td>`), CSS styles, and `<script>` blocks.
    - [ ] There is no duplicated content. The output represents a single, clean, and accurate summary.
    - [ ] Bullet points are formatted correctly using Markdown syntax (`-`).
