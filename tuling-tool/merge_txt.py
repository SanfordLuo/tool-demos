import os

txt_0 = "D:\\CodeOkay\\tuling-tool\\data\\单词_7309_7611.txt"
# txt_1 = "D:\\CodeOkay\\tuling-tool\\data\\test英文单词_1001_2000.txt"
# txt_2 = "D:\\CodeOkay\\tuling-tool\\data\\test英文单词_2001_3000.txt"
# txt_3 = "D:\\CodeOkay\\tuling-tool\\data\\test英文单词_3001_4000.txt"
# txt_4 = "D:\\CodeOkay\\tuling-tool\\data\\test英文单词_4001_5000.txt"

txt_list = [txt_0]
txt_ret = "D:\\CodeOkay\\tuling-tool\\data\\造课信息汇总0714_单词.txt"


def merge_data():
    ret_data = []
    for _txt in txt_list:
        with open(_txt, encoding='utf-8') as ff:
            _data = ff.readlines()

        print(f"child data: {len(_data)}")
        ret_data.extend(_data)

    print(f"未去重: {len(ret_data)}")

    idx_list = []
    ret_list = []
    for _ in ret_data:
        s_split = _.split(",", 1)
        if s_split[0] not in idx_list:
            ret_list.append(s_split)
            idx_list.append(s_split[0])

    ret_list.sort(key=lambda x: int(x[0]))
    print(f"已去重: {len(ret_list)}")

    if os.path.exists(txt_ret):
        raise Exception("txt_ret 文件名已存在")

    with open(txt_ret, "a", encoding="utf-8") as fw:
        for w_data in ret_list:
            fw.write(",".join(w_data))


if __name__ == '__main__':
    print("===== begin =====")
    merge_data()
    print("===== end =====")
