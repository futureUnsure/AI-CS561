import os
import inference
import unittest

class TestFinalOutputs(unittest.TestCase):

    #global inference.visited_facts
    #global inference.counter

    def setUp(self):
        pass

    def test_sample_input(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/input_1.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        os.system("cat output.txt")
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_sample_input.txt"), 0)

    def test_for_input_sent_by_TA(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/TA_test_1.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_TA_test_1.txt"), 0)


    def test_for_whatsapp_test_1(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_1.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_1.txt"), 0)

    def test_for_whatsapp_test_2(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_2.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        #self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_2.txt"), 0)


    def test_for_whatsapp_test_3(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_3.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_3.txt"), 0)


    def test_for_whatsapp_test_4(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_4.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_4.txt"), 0)


    def test_for_whatsapp_test_5(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_5.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_5.txt"), 0)

    def test_for_whatsapp_test_6(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_6.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_6.txt"), 0)

    def test_for_whatsapp_test_7(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_7.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_7.txt"), 0)

    def test_for_whatsapp_test_8(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_8.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_8.txt"), 0)

    def test_for_whatsapp_test_9(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/whatsapp_test_9.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_whatsapp_test_9.txt"), 0)

    def test_for_aniket_test_1(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/aniket_test_1.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_aniket_test_1.txt"), 0)

    def test_for_aniket_test_2(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/aniket_test_2.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_aniket_test_2.txt"), 0)


    def test_for_aniket_test_3(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/aniket_test_3.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_aniket_test_3.txt"), 0)

    
    def test_for_vasu_test_1(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/vasu_test_1.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_vasu_test_1.txt"), 0)

    def test_for_vasu_test_2(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/vasu_test_2.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_vasu_test_2.txt"), 0)


    def test_for_vasu_test_3(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/vasu_test_3.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        os.system("cat Testcases/correct_output_for_vasu_test_3.txt")
        os.system("cat output.txt")
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_vasu_test_3.txt"), 0)

    def test_for_vasu_test_4(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/vasu_test_4.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_vasu_test_4.txt"), 0)


    def test_for_vasu_test_5(self):
        #global inference.visited_facts
        #global inference.counter
        self.InputFileName = "Testcases/vasu_test_5.txt"
        self.OutputFileName = "output.txt"
        self.input_file_handle = open(self.InputFileName, 'r')
        self.output_file_handle = open(self.OutputFileName, 'w')
        #output_file_handle = open('output.txt','w')
        queries, KB = inference.read_logic_data(self.input_file_handle)
        for query in queries:
            try:
                result = "TRUE\n" if (len(list(inference.bc_ask(KB, query))) > 0)\
                        else "FALSE\n"
            except RuntimeError:
                #Hack to handle infinite loop in var names alone
                result = "FALSE\n"
            self.output_file_handle.write(result)
            inference.visited_facts = list()
            inference.counter = 0

        self.output_file_handle.close()
        self.input_file_handle.close()
        self.assertEqual(os.system("diff output.txt Testcases/correct_output_for_vasu_test_5.txt"), 0)

    def tearDown(self):
        #os.system("rm output.txt")
        pass


def main():
    #how to test for a single def
    #suite = unittest.TestSuite()
    #suite.addTest(TestFinalOutputs("test_sample_input"))
    #runner = unittest.TextTestRunner()
    #runner.run(suite)
    unittest.main()

if __name__ == '__main__':
    main()
