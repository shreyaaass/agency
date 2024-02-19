def delete_lines_inplace(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Open the file in write mode, truncating it
    with open(file_path, 'w') as file:
        for line in lines:
            # Check if the line should be deleted
            if line.find("category")==-1:
                # Write the line back to the file
                file.write(line)

# Example usage:
file_path = 'myMM_copy.txt' 
delete_lines_inplace(file_path)
