import { createClient, type SupabaseClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

/**
 * Supabase é opcional. Quando as variáveis de ambiente não estão presentes,
 * o app funciona em modo local (localStorage) — ideal para demo. Configure o
 * `.env.local` para ativar autenticação, banco e storage reais.
 */
export const supabaseEnabled = Boolean(url && anon);

let client: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient | null {
  if (!supabaseEnabled) return null;
  if (!client) {
    client = createClient(url!, anon!, {
      auth: { persistSession: true, autoRefreshToken: true },
    });
  }
  return client;
}
