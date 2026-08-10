class HashObject:
    def __init__(self):
        self.data = {}

    def set(self, field, value):
        """
        Insert a new field or update an existing field.
        """
        self.data[field] = value

    def get(self, field):
        """
        Return the value corresponding to the field.
        Returns None if the field does not exist.
        """
        return self.data.get(field)

    def delete(self, field):
        """
        Delete a field from the hash.
        Returns 1 if deleted, else 0.
        """
        if field in self.data:
            del self.data[field]
            return 1
        return 0

    def exists(self, field):
        """
        Check whether a field exists.
        """
        return field in self.data

    def size(self):
        """
        Number of fields in the hash.
        """
        return len(self.data)

    def keys(self):
        """
        Return all field names.
        """
        return list(self.data.keys())

    def values(self):
        """
        Return all values.
        """
        return list(self.data.values())

    def items(self):
        """
        Return all (field, value) pairs.
        """
        return list(self.data.items())

    def clear(self):
        """
        Remove all fields.
        """
        self.data.clear()