def increment_alpha(alpha):
    alpha_list = list(alpha)

    for i in range(len(alpha_list) - 1, -1, -1):
        if alpha_list[i] == "Z":
            alpha_list[i] = "A"
        else:
            alpha_list[i] = chr(ord(alpha_list[i]) + 1)
            break

    return "".join(alpha_list)
