
import { defineConfig } from "tinacms";

export default defineConfig({
  branch: "main",
  clientId: process.env.NEXT_PUBLIC_TINA_CLIENT_ID,
  token: process.env.TINA_TOKEN,
  build: {
    outputFolder: "admin",
    publicFolder: "public",
  },
  media: {
    tina: {
      mediaRoot: "images",
      publicFolder: "public",
    },
  },
  schema: {
    collections: [
      
      {
        name: "en_portal",
        label: "[EN] Portal",
        path: "content/en/portal",
        format: "json",
        ui: {
          // Don't let editors create new files if you want strict sync with code
          allowedActions: { create: true, delete: true },
        },
        fields: [
          {
            type: "string",
            name: "full_slug",
            label: "Slug",
            ui: { component: "hidden" }
          },
          {
            type: "object",
            name: "content",
            label: "Content Data",
            fields: [
              // --- Generated Fields based on your App ---
              {
                 type: "string",
                 name: "Text",
                 label: "Text",
                 ui: { component: "textarea" } 
              },
              {
                 type: "string",
                 name: "Title",
                 label: "Title"
              },
              {
                 type: "rich-text",
                 name: "SubText",
                 label: "Sub Text (Markdown)"
              },
              {
                 type: "rich-text",
                 name: "MainText",
                 label: "Main Text (Markdown)"
              },
              {
                 type: "string",
                 name: "BoxTitle",
                 label: "Box Title"
              },
              {
                 type: "string",
                 name: "TooltipText",
                 label: "Tooltip Text"
              },
              {
                 type: "string",
                 name: "ContentExample",
                 label: "Content Example"
              },
              // --- COMPLEX OBJECTS ---
              {
                type: "object",
                name: "PDF",
                label: "PDF Attachment",
                fields: [
                  { type: "image", name: "filename", label: "File" },
                  { type: "string", name: "alt", label: "Alt Text" }
                ]
              },
              {
                type: "object",
                name: "Icon",
                label: "Icon",
                fields: [
                  { type: "image", name: "filename", label: "Image" },
                  { type: "string", name: "name", label: "Name" }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Links",
                label: "Links",
                ui: { itemProps: (item) => ({ label: item?.title }) },
                fields: [
                  { type: "string", name: "title", label: "Title" },
                  { type: "string", name: "subtitle", label: "Subtitle" },
                  { 
                    type: "object", 
                    name: "link", 
                    label: "Link Target",
                    fields: [{ type: "string", name: "url", label: "URL" }]
                  }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Releases",
                label: "Releases",
                ui: { itemProps: (item) => ({ label: item?.ReleaseTitle }) },
                fields: [
                  { type: "string", name: "ReleaseTitle", label: "Version" },
                  { type: "datetime", name: "ReleaseDate", label: "Date" },
                  { type: "string", name: "Content", label: "Notes", ui: { component: "textarea" } }
                ]
              },
              // Add a generic 'catch-all' for other fields if needed, 
              // or define them explicitly here like Sveltia.
              {
                 type: "string",
                 name: "component",
                 label: "Component Type",
                 ui: { component: "hidden" }
              }
            ]
          }
        ]
      },

      {
        name: "de_portal",
        label: "[DE] Portal",
        path: "content/de/portal",
        format: "json",
        ui: {
          // Don't let editors create new files if you want strict sync with code
          allowedActions: { create: true, delete: true },
        },
        fields: [
          {
            type: "string",
            name: "full_slug",
            label: "Slug",
            ui: { component: "hidden" }
          },
          {
            type: "object",
            name: "content",
            label: "Content Data",
            fields: [
              // --- Generated Fields based on your App ---
              {
                 type: "string",
                 name: "Text",
                 label: "Text",
                 ui: { component: "textarea" } 
              },
              {
                 type: "string",
                 name: "Title",
                 label: "Title"
              },
              {
                 type: "rich-text",
                 name: "SubText",
                 label: "Sub Text (Markdown)"
              },
              {
                 type: "rich-text",
                 name: "MainText",
                 label: "Main Text (Markdown)"
              },
              {
                 type: "string",
                 name: "BoxTitle",
                 label: "Box Title"
              },
              {
                 type: "string",
                 name: "TooltipText",
                 label: "Tooltip Text"
              },
              {
                 type: "string",
                 name: "ContentExample",
                 label: "Content Example"
              },
              // --- COMPLEX OBJECTS ---
              {
                type: "object",
                name: "PDF",
                label: "PDF Attachment",
                fields: [
                  { type: "image", name: "filename", label: "File" },
                  { type: "string", name: "alt", label: "Alt Text" }
                ]
              },
              {
                type: "object",
                name: "Icon",
                label: "Icon",
                fields: [
                  { type: "image", name: "filename", label: "Image" },
                  { type: "string", name: "name", label: "Name" }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Links",
                label: "Links",
                ui: { itemProps: (item) => ({ label: item?.title }) },
                fields: [
                  { type: "string", name: "title", label: "Title" },
                  { type: "string", name: "subtitle", label: "Subtitle" },
                  { 
                    type: "object", 
                    name: "link", 
                    label: "Link Target",
                    fields: [{ type: "string", name: "url", label: "URL" }]
                  }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Releases",
                label: "Releases",
                ui: { itemProps: (item) => ({ label: item?.ReleaseTitle }) },
                fields: [
                  { type: "string", name: "ReleaseTitle", label: "Version" },
                  { type: "datetime", name: "ReleaseDate", label: "Date" },
                  { type: "string", name: "Content", label: "Notes", ui: { component: "textarea" } }
                ]
              },
              // Add a generic 'catch-all' for other fields if needed, 
              // or define them explicitly here like Sveltia.
              {
                 type: "string",
                 name: "component",
                 label: "Component Type",
                 ui: { component: "hidden" }
              }
            ]
          }
        ]
      },

      {
        name: "fr_portal",
        label: "[FR] Portal",
        path: "content/fr/portal",
        format: "json",
        ui: {
          // Don't let editors create new files if you want strict sync with code
          allowedActions: { create: true, delete: true },
        },
        fields: [
          {
            type: "string",
            name: "full_slug",
            label: "Slug",
            ui: { component: "hidden" }
          },
          {
            type: "object",
            name: "content",
            label: "Content Data",
            fields: [
              // --- Generated Fields based on your App ---
              {
                 type: "string",
                 name: "Text",
                 label: "Text",
                 ui: { component: "textarea" } 
              },
              {
                 type: "string",
                 name: "Title",
                 label: "Title"
              },
              {
                 type: "rich-text",
                 name: "SubText",
                 label: "Sub Text (Markdown)"
              },
              {
                 type: "rich-text",
                 name: "MainText",
                 label: "Main Text (Markdown)"
              },
              {
                 type: "string",
                 name: "BoxTitle",
                 label: "Box Title"
              },
              {
                 type: "string",
                 name: "TooltipText",
                 label: "Tooltip Text"
              },
              {
                 type: "string",
                 name: "ContentExample",
                 label: "Content Example"
              },
              // --- COMPLEX OBJECTS ---
              {
                type: "object",
                name: "PDF",
                label: "PDF Attachment",
                fields: [
                  { type: "image", name: "filename", label: "File" },
                  { type: "string", name: "alt", label: "Alt Text" }
                ]
              },
              {
                type: "object",
                name: "Icon",
                label: "Icon",
                fields: [
                  { type: "image", name: "filename", label: "Image" },
                  { type: "string", name: "name", label: "Name" }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Links",
                label: "Links",
                ui: { itemProps: (item) => ({ label: item?.title }) },
                fields: [
                  { type: "string", name: "title", label: "Title" },
                  { type: "string", name: "subtitle", label: "Subtitle" },
                  { 
                    type: "object", 
                    name: "link", 
                    label: "Link Target",
                    fields: [{ type: "string", name: "url", label: "URL" }]
                  }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Releases",
                label: "Releases",
                ui: { itemProps: (item) => ({ label: item?.ReleaseTitle }) },
                fields: [
                  { type: "string", name: "ReleaseTitle", label: "Version" },
                  { type: "datetime", name: "ReleaseDate", label: "Date" },
                  { type: "string", name: "Content", label: "Notes", ui: { component: "textarea" } }
                ]
              },
              // Add a generic 'catch-all' for other fields if needed, 
              // or define them explicitly here like Sveltia.
              {
                 type: "string",
                 name: "component",
                 label: "Component Type",
                 ui: { component: "hidden" }
              }
            ]
          }
        ]
      },

      {
        name: "it_portal",
        label: "[IT] Portal",
        path: "content/it/portal",
        format: "json",
        ui: {
          // Don't let editors create new files if you want strict sync with code
          allowedActions: { create: true, delete: true },
        },
        fields: [
          {
            type: "string",
            name: "full_slug",
            label: "Slug",
            ui: { component: "hidden" }
          },
          {
            type: "object",
            name: "content",
            label: "Content Data",
            fields: [
              // --- Generated Fields based on your App ---
              {
                 type: "string",
                 name: "Text",
                 label: "Text",
                 ui: { component: "textarea" } 
              },
              {
                 type: "string",
                 name: "Title",
                 label: "Title"
              },
              {
                 type: "rich-text",
                 name: "SubText",
                 label: "Sub Text (Markdown)"
              },
              {
                 type: "rich-text",
                 name: "MainText",
                 label: "Main Text (Markdown)"
              },
              {
                 type: "string",
                 name: "BoxTitle",
                 label: "Box Title"
              },
              {
                 type: "string",
                 name: "TooltipText",
                 label: "Tooltip Text"
              },
              {
                 type: "string",
                 name: "ContentExample",
                 label: "Content Example"
              },
              // --- COMPLEX OBJECTS ---
              {
                type: "object",
                name: "PDF",
                label: "PDF Attachment",
                fields: [
                  { type: "image", name: "filename", label: "File" },
                  { type: "string", name: "alt", label: "Alt Text" }
                ]
              },
              {
                type: "object",
                name: "Icon",
                label: "Icon",
                fields: [
                  { type: "image", name: "filename", label: "Image" },
                  { type: "string", name: "name", label: "Name" }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Links",
                label: "Links",
                ui: { itemProps: (item) => ({ label: item?.title }) },
                fields: [
                  { type: "string", name: "title", label: "Title" },
                  { type: "string", name: "subtitle", label: "Subtitle" },
                  { 
                    type: "object", 
                    name: "link", 
                    label: "Link Target",
                    fields: [{ type: "string", name: "url", label: "URL" }]
                  }
                ]
              },
              {
                type: "object",
                list: true,
                name: "Releases",
                label: "Releases",
                ui: { itemProps: (item) => ({ label: item?.ReleaseTitle }) },
                fields: [
                  { type: "string", name: "ReleaseTitle", label: "Version" },
                  { type: "datetime", name: "ReleaseDate", label: "Date" },
                  { type: "string", name: "Content", label: "Notes", ui: { component: "textarea" } }
                ]
              },
              // Add a generic 'catch-all' for other fields if needed, 
              // or define them explicitly here like Sveltia.
              {
                 type: "string",
                 name: "component",
                 label: "Component Type",
                 ui: { component: "hidden" }
              }
            ]
          }
        ]
      },

    ],
  },
});
