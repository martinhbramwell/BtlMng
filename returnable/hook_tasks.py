def startStockEntry(self, method):
    deliveryNote = self
    print("""#    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    """)
    print("""#    #    {}   """.format(method))
    deliveryNoteItems = deliveryNote.items
    for item in deliveryNoteItems:
        print("""#    #    {}   """.format(
            item.item_code,
            item.description
        ))
