# this many meaningful sequence in this many samples

# x in y

# find the hEN const, how many randoms create 1 meaning ful -- p&c qn

logic:
basic + cv-vc-cvc-ccv

db str:
table/document: 'words'

    word{
        exact_word_with_suffix_search
        length
        syllabi:[
            syllable:'name'
        ]
    }

swaranto/banjonanto --> no need to store can be calculated easily

# Res: ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
there is an inherent অ after some consonants, sometimes, that is based on pronounciation, this is hard to incorporate
মানুষ: ['মান্', 'ুষ্']
মানুষ: ['মা', 'নুষ্'] rule 1.3 is responsible for this
মানুষ: ['মা', 'নু', 'ষ্']

# no cvc, cv only,

বিধাতার: ['বি', 'ধা', 'তা', 'র্']
বিধাতার: ['বি', 'ধাত্', 'ার্']
আনারস: ['আ', 'না', 'রস্']
আনারস: ['আ', 'নার্', 'স্']

চলো: ['চলো'] here, eta ccv but we like to pronounce this as cc + v, but this is also valid and can be pronounced at once

বিদ্যালয়: ['বি', 'দ্', 'যাল্', 'য়'] # ekhane abar bid hobe bi noi, cv te kata cholbe na

so exact hochhe na but syllabi are valic, it would have been better to just create random cvc cv vc ccv strings,
but most of them will not create meningful words

# Best process will be to add weights to every letter and some common combinations, and break after a thresold is reacheds

# first we need to consider the length and commonness of the word also, as the pronounciation changes based on how ofthen the word is used

# for poem it will be ok even if we ignore the commonness and check for ideal syllabi

# but the length and constituents will has to be considered

বাংলা: ['বা', 'ং', 'লা']
মানুষ: ['মা', 'নুষ্']
মা: ['মা']
দোলনা: ['দো', 'লনা']
পরিবার: ['পরি', 'বার্']
বন্ধু: ['বন্', 'ধু']
বিদ্যালয়: ['বি', 'দ্', 'যাল্', 'য়']
বিশ্ববিদ্যালয়: ['বি', 'শ্', 'ববি', 'দ্', 'যাল্', 'য়']
রবীন্দ্রনাথ: ['রবী', 'ন্দ্', 'রনা', 'থ্']

বিধাতার: ['বি', 'ধাত্', 'ার্']
আনারস: ['আ', 'নার্', 'স্']

# with 1.3

তুমি: ['তু', 'মি']
আকাশ: ['আ', 'কাশ্']
কলম: ['ক্', 'লম্']
চলো: ['চলো']
বাংলা: ['বা', 'ং', 'লা']
মানুষ: ['মা', 'নুষ্']
মা: ['মা']
দোলনা: ['দো', 'লনা']
পরিবার: ['পরি', 'বার্']
বন্ধু: ['বন্', 'ধু']
বিদ্যালয়: ['বি', 'দ্', 'যাল্', 'য়']
বিশ্ববিদ্যালয়: ['বি', 'শ্', 'ববি', 'দ্', 'যাল্', 'য়']
রবীন্দ্রনাথ: ['রবী', 'ন্দ্', 'রনা', 'থ্']
বিধাতার: ['বি', 'ধাত্', 'ার্']
আনারস: ['আ', 'নার্', 'স্']

# without 1.3

তুমি: ['তুম্', 'ই']
আকাশ: ['আ', 'কাশ্']
কলম: ['ক্', 'লম্']
চলো: ['চলো']
বাংলা: ['বা', 'ং', 'লা']
মানুষ: ['মান্', 'ুষ্']
মা: ['মা']
দোলনা: ['দোল্', 'না']
পরিবার: ['পরি', 'বার্']
বন্ধু: ['বন্', 'ধু']
বিদ্যালয়: ['বিদ্', '্', 'যাল্', 'য়']
বিশ্ববিদ্যালয়: ['বিশ্', '্', 'ববি', 'দ্', 'যাল্', 'য়']
রবীন্দ্রনাথ: ['রবী', 'ন্দ্', 'রনা', 'থ্']
বিধাতার: ['বিধ্', 'াত্', 'ার্']
আনারস: ['আ', 'নার্', 'স্']
'''
