import sys

files = list()
freespace = list()

with open(sys.argv[1]) as f:
    is_file = True
    file_id = 0
    disk_size = 0
    for c in f.read().strip():
        size = int(c)
        if is_file:
            files.append((file_id, size))
            file_id += 1
        else:
            freespace.append(size)
        disk_size += size
        is_file = not is_file

def defrag_by_block(files, freespace):
    defragged = []
    defrag_file = len(files)-1
    for i in range(0,len(freespace)):
        if files[i] == None:
            break
        defragged.append(files[i])
        files[i] = None

        while True:
            if files[defrag_file] == None:
                break
            if files[defrag_file][1] >= freespace[i]:
                defragged.append((files[defrag_file][0], freespace[i]))
                if files[defrag_file][1] == freespace[i]:
                    files[defrag_file] = None
                    defrag_file -= 1
                else:
                    files[defrag_file] = (files[defrag_file][0], files[defrag_file][1]-freespace[i])
                break

            defragged.append(files[defrag_file])
            freespace[i] -= files[defrag_file][1]
            files[defrag_file] = None
            defrag_file -= 1

    return defragged

def calc_checksum(files):
    pos = 0
    checksum = 0
    for (fid, size) in files:
        c = int((pos + pos + size - 1)*size/2)
        checksum += c*fid
        pos += size
    return checksum


defragged = defrag_by_block(files[:], freespace[:])
print(calc_checksum(defragged))
