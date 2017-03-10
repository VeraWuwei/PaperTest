class ListNode:
    def __init__(self,x):
        self.val=x
        self.next=None

def nonrecurse(head):
    if head is None or head.next is None:
        return head
    pre=None
    cur=head
    h=head
    while cur:
        h=cur
        tmp=cur.next
        cur.next=pre
        pre=cur
        cur=tmp
    return h
    
head=ListNode(1)
p1=ListNode(2)
p2=ListNode(3)
p3=ListNode(4)
head.next=p1
p1.next=p2
p2.next=p3
p=nonrecurse(head)
while p:
    print p.val
    p=p.next