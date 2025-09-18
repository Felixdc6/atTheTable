-- At The Table Database Schema
-- This file contains the complete database schema for the bill splitting app

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE item_category AS ENUM ('Food', 'Drinks');
CREATE TYPE item_type AS ENUM ('item', 'surcharge');

-- Bills table
CREATE TABLE bills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_id UUID, -- Will be linked to auth.users when auth is implemented
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    link_token_hash VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_locked BOOLEAN DEFAULT FALSE
);

-- Participants table
CREATE TABLE participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bill_id UUID NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    is_payer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Items table
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bill_id UUID NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    category item_category NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    qty_total INTEGER NOT NULL DEFAULT 1,
    type item_type NOT NULL DEFAULT 'item',
    qty_shared_pool INTEGER DEFAULT 0,
    confidence DECIMAL(3,2) DEFAULT 1.0, -- 0.00 to 1.00
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Claims table (exclusive claims)
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bill_id UUID NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
    item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    participant_id UUID NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    qty_claimed INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(item_id, participant_id)
);

-- Shared members table (for shared pools)
CREATE TABLE shared_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    participant_id UUID NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(item_id, participant_id)
);

-- Submissions table (participant confirmations)
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bill_id UUID NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
    participant_id UUID NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(bill_id, participant_id)
);

-- Indexes for performance
CREATE INDEX idx_bills_link_token ON bills(link_token_hash);
CREATE INDEX idx_participants_bill_id ON participants(bill_id);
CREATE INDEX idx_items_bill_id ON items(bill_id);
CREATE INDEX idx_claims_bill_id ON claims(bill_id);
CREATE INDEX idx_claims_item_id ON claims(item_id);
CREATE INDEX idx_shared_members_item_id ON shared_members(item_id);
CREATE INDEX idx_submissions_bill_id ON submissions(bill_id);

-- Functions for calculations
CREATE OR REPLACE FUNCTION calculate_remaining_qty(item_uuid UUID)
RETURNS INTEGER AS $$
DECLARE
    total_qty INTEGER;
    exclusive_claimed INTEGER;
    shared_pool_qty INTEGER;
BEGIN
    -- Get total quantity
    SELECT qty_total INTO total_qty FROM items WHERE id = item_uuid;
    
    -- Get exclusive claims
    SELECT COALESCE(SUM(qty_claimed), 0) INTO exclusive_claimed 
    FROM claims WHERE item_id = item_uuid;
    
    -- Get shared pool quantity
    SELECT COALESCE(qty_shared_pool, 0) INTO shared_pool_qty 
    FROM items WHERE id = item_uuid;
    
    RETURN total_qty - exclusive_claimed - shared_pool_qty;
END;
$$ LANGUAGE plpgsql;

-- Function to get participant totals
CREATE OR REPLACE FUNCTION get_participant_totals(bill_uuid UUID)
RETURNS TABLE (
    participant_id UUID,
    participant_name VARCHAR,
    exclusive_total DECIMAL,
    shared_total DECIMAL,
    grand_total DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.name,
        COALESCE(SUM(i.unit_price * c.qty_claimed), 0) as exclusive_total,
        COALESCE(
            SUM(i.unit_price * i.qty_shared_pool / 
                NULLIF((SELECT COUNT(*) FROM shared_members sm WHERE sm.item_id = i.id), 0)
            ), 0
        ) as shared_total,
        COALESCE(SUM(i.unit_price * c.qty_claimed), 0) + 
        COALESCE(
            SUM(i.unit_price * i.qty_shared_pool / 
                NULLIF((SELECT COUNT(*) FROM shared_members sm WHERE sm.item_id = i.id), 0)
            ), 0
        ) as grand_total
    FROM participants p
    LEFT JOIN claims c ON c.participant_id = p.id
    LEFT JOIN items i ON i.id = c.item_id AND i.bill_id = bill_uuid
    LEFT JOIN shared_members sm ON sm.participant_id = p.id AND sm.item_id = i.id
    WHERE p.bill_id = bill_uuid
    GROUP BY p.id, p.name;
END;
$$ LANGUAGE plpgsql;

-- Row Level Security (RLS) policies
-- Note: These will be refined when auth is implemented

-- Enable RLS on all tables
ALTER TABLE bills ENABLE ROW LEVEL SECURITY;
ALTER TABLE participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- Basic policies (will be updated with proper auth)
-- For now, allow all operations (will be restricted later)
CREATE POLICY "Allow all operations on bills" ON bills FOR ALL USING (true);
CREATE POLICY "Allow all operations on participants" ON participants FOR ALL USING (true);
CREATE POLICY "Allow all operations on items" ON items FOR ALL USING (true);
CREATE POLICY "Allow all operations on claims" ON claims FOR ALL USING (true);
CREATE POLICY "Allow all operations on shared_members" ON shared_members FOR ALL USING (true);
CREATE POLICY "Allow all operations on submissions" ON submissions FOR ALL USING (true);
