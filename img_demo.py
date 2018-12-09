    imagePath = '../image/00004.jpg'
    ocrSlice = (125, 185, 160, 700)  # (90, 150, 225, 850)  # (125, 185, 160, 700)

    cropImg = Image.open(imagePath).convert('L')
    # cropImg.save('hui.jpg')
    #
    # image = Image.open('hui.jpg')
    image = np.array(cropImg)[ocrSlice[0]:ocrSlice[1], ocrSlice[2]:ocrSlice[3]]
    text = pytesseract.image_to_string(image, 'chi_sim')
