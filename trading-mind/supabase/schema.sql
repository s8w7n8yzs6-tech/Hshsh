-- ═══════════════════════════════════════════════════════════════
-- Trading Mind — Schema Supabase
-- Autenticação nativa (auth.users) + perfis, diários, operações,
-- eventos do freio de emergência e análises de IA.
-- Row Level Security garante que cada trader vê apenas os próprios dados.
-- ═══════════════════════════════════════════════════════════════

-- ── PERFIS ─────────────────────────────────────────────────────
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  name text,
  email text,
  -- configuração da mesa/desafio
  meta_mesa numeric default 6000,
  drawdown_maximo numeric default 4000,
  meta_lucro_dia numeric default 500,
  duracao_desafio int default 30,
  saldo_inicial_mesa numeric default 50000,
  inicio_desafio date default current_date,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- ── DIÁRIOS (SESSÕES) ──────────────────────────────────────────
create table if not exists public.sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  data date not null,
  pre jsonb not null default '{}'::jsonb,          -- pré-mercado + checklist
  psychology jsonb not null default '{}'::jsonb,   -- etapa psicologia
  self_eval jsonb not null default '{}'::jsonb,    -- notas 0-100
  reflection jsonb not null default '{}'::jsonb,   -- reflexão
  analysis jsonb,                                  -- análise da IA
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique (user_id, data)
);

-- ── OPERAÇÕES ──────────────────────────────────────────────────
create table if not exists public.trades (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.sessions(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  ativo text,
  direcao text check (direcao in ('compra','venda')),
  horario text,
  setup text,
  lote numeric,
  stop numeric,
  take numeric,
  resultado numeric default 0,
  screenshot text,           -- caminho no Storage
  observacoes text,
  brake_override boolean default false,
  created_at timestamptz default now()
);

-- ── FREIO DE EMERGÊNCIA ────────────────────────────────────────
create table if not exists public.brake_events (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references public.sessions(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  stops_hoje int,
  saldo_status text,
  motivo text,               -- 'setup' | 'recuperar'
  emocional int,             -- 0-10
  dormiu_bem boolean,
  cansado boolean,
  ansioso boolean,
  risco_alto boolean,
  decisao text,              -- 'continuou' | 'voltou'
  created_at timestamptz default now()
);

-- ── CONQUISTAS ─────────────────────────────────────────────────
create table if not exists public.achievements (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  key text not null,
  unlocked_at timestamptz default now(),
  unique (user_id, key)
);

-- ── ÍNDICES ────────────────────────────────────────────────────
create index if not exists idx_sessions_user on public.sessions(user_id, data);
create index if not exists idx_trades_session on public.trades(session_id);
create index if not exists idx_brake_user on public.brake_events(user_id);

-- ═══════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY
-- ═══════════════════════════════════════════════════════════════
alter table public.profiles enable row level security;
alter table public.sessions enable row level security;
alter table public.trades enable row level security;
alter table public.brake_events enable row level security;
alter table public.achievements enable row level security;

-- Perfis
drop policy if exists "own profile" on public.profiles;
create policy "own profile" on public.profiles
  for all using (auth.uid() = id) with check (auth.uid() = id);

-- Sessões
drop policy if exists "own sessions" on public.sessions;
create policy "own sessions" on public.sessions
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Operações
drop policy if exists "own trades" on public.trades;
create policy "own trades" on public.trades
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Freio
drop policy if exists "own brake" on public.brake_events;
create policy "own brake" on public.brake_events
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Conquistas
drop policy if exists "own achievements" on public.achievements;
create policy "own achievements" on public.achievements
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════
-- Cria perfil automaticamente ao registrar usuário
-- ═══════════════════════════════════════════════════════════════
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, name, email)
  values (new.id, coalesce(new.raw_user_meta_data->>'name', split_part(new.email,'@',1)), new.email)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ═══════════════════════════════════════════════════════════════
-- STORAGE — bucket para screenshots das operações
-- ═══════════════════════════════════════════════════════════════
insert into storage.buckets (id, name, public)
values ('screenshots', 'screenshots', true)
on conflict (id) do nothing;

drop policy if exists "own screenshots upload" on storage.objects;
create policy "own screenshots upload" on storage.objects
  for insert with check (bucket_id = 'screenshots' and auth.uid()::text = (storage.foldername(name))[1]);

drop policy if exists "screenshots readable" on storage.objects;
create policy "screenshots readable" on storage.objects
  for select using (bucket_id = 'screenshots');
