def convert_p6_to_p3(input_file, output_file):
    with open(input_file, 'rb') as f:
        magic_number = f.readline().strip()
        if magic_number != b'P6':
            raise ValueError("입력 파일은 P6 포맷이 아닙니다.")

        
        line = f.readline()
        while line.startswith(b'#'):
            line = f.readline()

        width, height = map(int, line.strip().split())

        maxval = int(f.readline().strip())

        
        pixel_data = f.read()

    
    with open(output_file, 'w') as out:
        out.write("P3\n")
        out.write(f"{width} {height}\n")
        out.write(f"{maxval}\n")

        for i in range(0, len(pixel_data), 3):
            r = pixel_data[i]
            g = pixel_data[i + 1]
            b = pixel_data[i + 2]
            out.write(f"{r} {g} {b}\n")

convert_p6_to_p3("/home/data/colorP6File.ppm", "colorP3File.ppm")

