import en, { type Messages } from "@/messages/en";

export const defaultLocale = "en";
export const messages: Record<string, Messages> = { en };

export function getMessages(locale = defaultLocale): Messages {
  return messages[locale] ?? en;
}

