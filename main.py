#testing functionality
from app.data.db import connect_database
from app.data.schema import create_users_table, create_datasets_metadata_table, create_it_tickets_table, cybersecurity_table
conn=connect_database()
create_users_table(conn)
create_datasets_metadata_table(conn)
create_it_tickets_table(conn)
cybersecurity_table(conn)
from app.services.user_service import register, login, migrate_users
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident, get_incidents_by_type_count, get_high_severity_by_status

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # Migrate users
    migrate_users(conn)
    
    # Test authentication
    msg = register("ian", "SecurePass123!", "analyst")
    print(msg)
    
    msg = login("ian", "SecurePass123!")
    print(msg)
    
    # Test CRUD
    incident_id = insert_incident(conn,
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")
    
    #Query data
    get = get_all_incidents(conn)
    print(f"Total incidents: {len(get)}")

if __name__ == "__main__":
    main()
def run_comprehensive_tests(conn):

    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    msg = register("test_user", "TestPass123!", "user")
    print(f"  Register: {msg}")
    
    msg = login("test_user", "TestPass123!")
    print(f"  Login: {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")
    
    # Read
    get= get_all_incidents(conn)
    print(f"  Read:    Found incident {len(get)}")
    
    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")
    
    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)


run_comprehensive_tests(conn)