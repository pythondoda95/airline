from file_handling.reservation_service import ReservationService

service = ReservationService()

layout_name = "economy.txt"
seat = "2B"

print("TEST 1: Non-admin cannot cancel others")
user_id = 2
username = "normal_user"
is_admin = False

success = service.admin_cancel(user_id, username, is_admin, layout_name, seat)
print("Should be False:", success)


print("\nTEST 2: Admin can cancel reservation")
admin_id = 1
admin_name = "admin"
admin_is_admin = True

# Reserve seat first
service.reserve(admin_id, admin_name, layout_name, seat)

success = service.admin_cancel(admin_id, admin_name, admin_is_admin, layout_name, seat)
print("Should be True:", success)


print("\nTEST 3: User can cancel own reservation, but not others")

# User reserves seat
user_id = 3
username = "user3"
is_admin = False

service.reserve(user_id, username, layout_name, seat)

# Same user cancels own seat
success = service.cancel_own(user_id, username, layout_name, seat)
print("Own cancel should be True:", success)

# Admin reserves again (for next test)
service.reserve(admin_id, admin_name, layout_name, seat)

# Different user tries to cancel admin reservation
success = service.cancel_own(user_id, username, layout_name, seat)
print("Cancel other user's seat should be False:", success)

# Clean up (admin removes seat)
service.admin_cancel(admin_id, admin_name, admin_is_admin, layout_name, seat)
