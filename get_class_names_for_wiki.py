from sub_occs import sub_of_occurence
from sub_orgs import sub_of_organisation
from sub_arts import sub_of_artist

# Script for getting classess for wiki updates
if __name__ == '__main__':
    with open("org", "w") as f:
        for i, ii in enumerate(sub_of_organisation.values()):
            f.write(str(ii[0]) + ",\n" if (i + 1) % 5 == 0 else str(ii[0]) + ", ")
    f.close()
    with open("occ", "w") as f:
        for i, ii in enumerate(sub_of_occurence.values()):
            f.write(str(ii[0]) + ",\n" if (i + 1) % 5 == 0 else str(ii[0]) + ", ")
    f.close()
    with open("art", "w") as f:
        for i, ii in enumerate(sub_of_artist.values()):
            f.write(str(ii[0]) + ",\n" if (i + 1) % 5 == 0 else str(ii[0]) + ", ")
    f.close()
