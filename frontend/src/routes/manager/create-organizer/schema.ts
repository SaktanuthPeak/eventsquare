import { z } from "zod";

export const organizeSchema = z.object({
  name: z.string().min(1, "Organization name is required"),
  manager_id: z.string().default(""),
  co_manager_id: z.array(z.string()).default([]),
  staffs_id: z.array(z.string()).default([]),
  maximum_event: z
    .number()
    .int()
    .positive("Maximum events must be at least 1")
    .default(3),

  contact_information: z.object({
    email: z
      .string()
      .email("Please enter a valid email address")
      .or(z.literal("")),
    line_id: z.string().default(""),
    facebook: z.string().default(""),
    instagram: z.string().default(""),
    website_url: z
      .string()
      .url("Please enter a valid website URL")
      .or(z.literal(""))
      .default(""),
  }),

  business_address: z.object({
    company_name: z.string().min(1, "Company name is required").default(""),
    company_address: z
      .string()
      .min(1, "Company address is required")
      .default(""),
    company_phone: z
      .string()
      .min(1, "Company phone is required")
      .regex(
        /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,4}[-\s.]?[0-9]{1,9}$/,
        "Please enter a valid phone number"
      ),
  }),

  banking_information: z.object({
    bank_name: z.enum(
      [
        "ธนาคารกรุงไทย",
        "ธนาคารกรุงเทพ",
        "ธนาคารกสิกรไทย",
        "ธนาคารไทยพาณิชย์",
        "ธนาคารกรุงศรีอยุธยา",
      ],
      {
        errorMap: () => ({ message: "Please select a valid bank" }),
      }
    ),
    account_number: z
      .string()
      .min(10, "Account number must be at least 10 digits")
      .max(15, "Account number must not exceed 15 digits")
      .regex(/^\d+$/, "Account number must contain only digits"),
    account_name: z.string().min(1, "Account name is required"),
  }),
});

// Add a type for TypeScript support
export type OrganizeFormType = z.infer<typeof organizeSchema>;
