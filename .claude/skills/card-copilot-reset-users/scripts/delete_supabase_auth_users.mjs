#!/usr/bin/env node

const args = process.argv.slice(2);

const options = {
  email: null,
  all: false,
  dryRun: false,
  confirm: false,
};

for (let i = 0; i < args.length; i += 1) {
  const arg = args[i];
  if (arg === '--email') {
    options.email = (args[i + 1] || '').trim().toLowerCase();
    i += 1;
  } else if (arg === '--all') {
    options.all = true;
  } else if (arg === '--dry-run') {
    options.dryRun = true;
  } else if (arg === '--confirm') {
    options.confirm = true;
  } else if (arg === '-h' || arg === '--help') {
    printUsage(0);
  } else {
    console.error(`Unknown argument: ${arg}`);
    printUsage(1);
  }
}

if ((options.email ? 1 : 0) + (options.all ? 1 : 0) !== 1) {
  console.error('Provide exactly one scope: --email <value> OR --all');
  printUsage(1);
}

if (!options.dryRun && !options.confirm) {
  console.error('Refusing to delete without --confirm. Use --dry-run first.');
  process.exit(1);
}

const supabaseUrl = process.env.SUPABASE_URL || process.env.EXPO_PUBLIC_SUPABASE_URL;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !serviceRoleKey) {
  console.error('Missing required environment variables: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY');
  process.exit(1);
}

const baseUrl = supabaseUrl.replace(/\/$/, '');
const headers = {
  apikey: serviceRoleKey,
  Authorization: `Bearer ${serviceRoleKey}`,
  'Content-Type': 'application/json',
};

function printUsage(exitCode) {
  console.log(`Usage:
  node delete_supabase_auth_users.mjs --email tester@example.com --dry-run
  node delete_supabase_auth_users.mjs --email tester@example.com --confirm
  node delete_supabase_auth_users.mjs --all --dry-run
  node delete_supabase_auth_users.mjs --all --confirm`);
  process.exit(exitCode);
}

async function fetchUsersPage(page) {
  const url = `${baseUrl}/auth/v1/admin/users?page=${page}&per_page=100`;
  const response = await fetch(url, { method: 'GET', headers });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Failed listing users (${response.status}): ${body}`);
  }
  const payload = await response.json();
  return Array.isArray(payload.users) ? payload.users : [];
}

async function fetchAllUsers() {
  const users = [];
  let page = 1;
  while (true) {
    const chunk = await fetchUsersPage(page);
    users.push(...chunk);
    if (chunk.length < 100) break;
    page += 1;
  }
  return users;
}

async function deleteUser(userId) {
  const url = `${baseUrl}/auth/v1/admin/users/${encodeURIComponent(userId)}`;
  const response = await fetch(url, { method: 'DELETE', headers });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Failed deleting user ${userId} (${response.status}): ${body}`);
  }
}

(async () => {
  const allUsers = await fetchAllUsers();

  const selected = allUsers.filter((user) => {
    const email = String(user?.email || '').toLowerCase();
    if (options.all) return true;
    return email === options.email;
  });

  if (selected.length === 0) {
    console.log('No matching Auth users found.');
    return;
  }

  console.log(`Matched ${selected.length} user(s):`);
  for (const user of selected) {
    console.log(`- ${user.id}  ${user.email || '(no email)'}`);
  }

  if (options.dryRun) {
    console.log('Dry run only. No deletions executed.');
    return;
  }

  let deleted = 0;
  for (const user of selected) {
    await deleteUser(user.id);
    deleted += 1;
    console.log(`Deleted: ${user.id}  ${user.email || '(no email)'}`);
  }

  console.log(`Deletion complete. Deleted ${deleted} user(s).`);
})().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
