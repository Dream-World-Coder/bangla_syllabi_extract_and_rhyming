# this many meaningful sequence in this many samples

# x in y

# find the hEN const, how many randoms create 1 meaning ful -- p&c qn

logic:
basic + cv-vc-cvc-ccv

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

for stanza in range(no_of_stanza):

<!--  -->

    for lines in range(no_of_lines_per_stanza):
     <!--  -->
        for matra in extracted_pattern:
            print(f'{matra=}')
            # words_list.find =>
            # word or words for which
            # word.totalMatra.[chhondo] = matra
            # or, SumESum(word.totalMatra.[chhondo]) = matra // in sumesum check: matra > 0 must
            # now after you find them, store them temporarily because in most of the cases matra will be repeatitive (eg 7n+2, m*n+k)
            # now:
                # randomly pic any one word [easiest] -- current implementation
                # check parts of speech (word.partsOfSpeech) & pick any random based on a grammar^^^
                # ^^^[-- in poem usually s-v-o is not followed, it can be anything so grammer one will be skipped for now]
                # check মিল of last word, eg: বনে - মনে
                # alongside grammar check meaning & correspondance with previous words{something like correlation available here?} also and then pick one [hardest]

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# output: random:

['আইসক্রিম', 'লাফিয়েছিল', 'উইন']
['কুসুমবাসিত', 'বালিকারা', 'কোদাল']

    কৃতজ্ঞতার নামিয়াছে বিপদ্
    অনুরোধে দীর্ঘিকার ভাবিল

    চক্রবৃদ্ধি বার্ধক্যরেখা চাচাদেরও অপরিচয়
    সত্যপুরুষটি ট্রিনিটি পরিকল্পনার দাখো

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
