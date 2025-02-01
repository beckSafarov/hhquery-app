from configs import pro_roles_full

def get_role_id(selected_label):
  return next(field['id'] for field in pro_roles_full if field['label'] == selected_label)
