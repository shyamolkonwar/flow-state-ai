-- Query to get user IDs from the auth.users table
-- Run this to find a user ID to use in the seed_settings.sql file

SELECT
    id,
    email,
    created_at,
    last_sign_in_at
FROM auth.users
ORDER BY created_at DESC
LIMIT 10;

-- Alternative: If you want to see all users
-- SELECT id, email, created_at FROM auth.users ORDER BY created_at DESC;
