-- University Info Table Creation SQL Commands
-- Create table for storing university information by categories

CREATE TABLE university_info (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    info TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add index for better performance on category searches
CREATE INDEX idx_university_info_category ON university_info(category);

-- Create function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_university_info_updated_at 
    BEFORE UPDATE ON university_info
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data (optional)
INSERT INTO university_info (category, info) VALUES 
('overview', 'Dawood University of Engineering & Technology (DUET) is a renowned public engineering institution located in Karachi, Pakistan.'),
('history', 'Originally established in 1962 as Dawood College of Engineering and Technology (DCET), through a generous contribution from the Dawood Foundation.'),
('campus', 'DUET operates from two main campuses in Karachi. The Main Campus is situated near Mazar-e-Quaid on New M.A. Jinnah Road.'),
('undergraduate_programs', 'DUET offers Bachelor of Engineering (BE) degrees in Chemical Engineering, Computer Systems Engineering, Electronic Engineering, and more.'),
('postgraduate_programs', 'DUET provides MS and PhD programs in selected engineering fields including Chemical Engineering, Electronic Engineering, and Industrial Engineering.'),
('admission_criteria', 'For undergraduate admissions, applicants must have a minimum of 60% marks in HSC and pass the DUET Entry Test.');
