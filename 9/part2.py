import sys

freespace = list()
files = dict()

class File:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size


with open(sys.argv[1]) as f:
    is_file = True
    num_files = 0
    disk_size = 0
    for c in f.read().strip():
        size = int(c)
        if is_file:
            files[num_files] = File(disk_size, size)
            num_files += 1
        else:
            freespace.append(File(disk_size, size))
        disk_size += size
        is_file = not is_file


def defrag_by_file(files, freespace):
    for file_id in range(num_files-1,0,-1):
        for i in range(0,len(freespace)):
            if freespace[i] is None:
                continue
            
            if freespace[i].pos > files[file_id].pos:
                break

            if freespace[i].size >= files[file_id].size:
                files[file_id].pos = freespace[i].pos
            
                if freespace[i].size > files[file_id].size:
                    freespace[i].pos += files[file_id].size
                    freespace[i].size -= files[file_id].size
                else:
                    freespace[i] = None
    


def calc_checksum(files):
    pos = 0
    checksum = 0
    for (fid, f) in files.items():
        c = int((f.pos + f.pos + f.size - 1)*f.size/2)
        checksum += c*fid
    return checksum


defrag_by_file(files, freespace)
print(calc_checksum(files))
