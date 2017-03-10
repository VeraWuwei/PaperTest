class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def shift(self, data):
        new_node      = Node(data)
        new_node.next = self.head
        self.head     = new_node

    def smallerThanK(self, head, k):
        currentNode = head
        count       = 0

        while currentNode is not None and count < k:
            currentNode = currentNode.next
            count      += 1

        return currentNode is None

    def reverse(self, head, k):
        if self.smallerThanK(head, k):
            return head

        currentNode = head 
        nextNode    = None
        prevNode    = None
        count       = 0

        while currentNode is not None and count < k:
            nextNode         = currentNode.next
            currentNode.next = prevNode
            prevNode         = currentNode
            currentNode      = nextNode
            count           += 1

        if nextNode is not None:
            head.next = self.reverse(nextNode, k)

        return prevNode

    def printList(self):
        cur = self.head
        while(cur):
            print cur.data,
            cur = cur.next
        print ""

l = LinkedList()
l.shift(8)
l.shift(7)
l.shift(6)
l.shift(5)
l.shift(4)
l.shift(3)
l.shift(2)
l.shift(1)

l.printList()
l.head = l.reverse(l.head, 3)
l.printList()