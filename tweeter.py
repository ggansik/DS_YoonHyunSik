import sys

INFTY = 1E10
WHITE = 0
GRAY = 1
BLACK = 2




def v_merge(tmp,A,p,q,r):
    for i in range(p,r):
        tmp[i] = A[i]
    i = p
    j = q
    while i < q and j < r:
        if tmp[i].idN < tmp[j].idN:
            A[p] = tmp[i]
            i = i + 1
        else:
            A[p] = tmp[j]
            j = j + 1
        p = p + 1
    while i < q:
        A[p] = tmp[i]
        i = i + 1
        p = p + 1
    while j < r:
        A[p] = tmp[j]
        j = j + 1
        p = p + 1

def v_mergesort(tmp, A,p,r):
    if p < r - 1:
        q = (p + r) // 2
        v_mergesort(tmp, A,p,q)
        v_mergesort(tmp, A,q,r)
        v_merge(tmp, A,p,q,r)
class Heap:
    def __init__(self):
        self.nelem = 0
        self.A = []
    def parent(self,n):
        return (n-1)//2
    def left(self,n):
        return 2*n+1
    def right(self,n):
        return 2*n+2
    def compare(self,a,b):
        return a - b > 0
    def exchange(self,i,j):
        A = self.A
        A[i],A[j] = A[j],A[i]
    def heapify(self,i):
        A = self.A
        l = self.left(i)
        r = self.right(i)
        if l < self.nelem and self.compare(A[l], A[i]):
            largest = l
        else:
            largest = i
        if r < self.nelem and self.compare(A[r], A[largest]):
            largest = r
        if largest != i:
            self.exchange(i,largest)
            self.heapify(largest)

class PrioNode:
    def __init__(self, key, n):
        self.ndx = 0
        self.n = n
        self.key = key
    def __repr__(self):
        return "(%d:%d,%d)" % (self.ndx,self.n, self.key)

class MaxQueue(Heap):
    def __init__(self):
        super().__init__()
    def compare(self,a,b):
        return a.key > b.key
    def exchange(self,i,j):
        A = self.A
        A[i].ndx = j
        A[j].ndx = i
        super().exchange(i,j)
    def update_key(self,i):
        parent = lambda x: self.parent(i)
        compare = lambda a,b: self.compare(a,b)
        A = self.A
        while i > 0 and not compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)
    def increase_key(self,i,key):
        A = self.A
        if key < A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)
    def insert(self,n):
        A = self.A
        while (len(A) < self.nelem):
            A.append(None)
        i = self.nelem
        A.append(None)
        self.nelem = self.nelem + 1
        A[i] = n
        A[i].ndx = i
        self.update_key(i)
    def extract(self):
        elem = self.A[0]
        self.exchange(0,self.nelem-1)
        self.nelem = self.nelem - 1
        self.heapify(0)
        return elem
    def is_empty(self):
        return self.nelem == 0

class MinQueue(MaxQueue):
    def __init__(self):
        super().__init__()
    def compare(self,a,b):
        return a.key < b.key
    def update_key(self,i):
        parent = lambda x: self.parent(i)
        A = self.A
        while i > 0 and not self.compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)
    def decrease_key(self,i,key):
        A = self.A
        if key > A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)
    def __repr__(self):
        return "%a %a" % (self.nelem,self.A)

class Adj:
    def __init__(self):
        self.idN = ""
        self.screenName = ""
        self.date = ""
        self.n = 0
        self.next = None

class Vertex:
    def __init__(self, name):
        self.parent = -1
        self.name = name
        self.n = 0
        self.first = None
    def add(self, v):
        a = Adj()
        a.n = v.n
        a.next = self.first
        self.first = a
    def copy(self, other):
        self.parent = other.parent
        self.name = other.name
        self.n = other.n
        self.first = other.first

class userVertex:
    def __init__(self):
        self.parent = -1
        self.color = WHITE
        self.d = 0
        self.f = 0
        self.screenName = ""
        self.date = ""
        self.idN = ""
        self.n = 0
        self.tweets = []
        self.tweetnum = 0
        self.friendnum = 0
        self.first = None
    def add(self, v):
        a = Adj()
        a.idN = v.idN
        a.screenName = v.screenName
        a.date = v.date
        a.next = self.first
        self.first = a
    def copy (self, other):
        self.parent = other.parent
        self.color = other.color
        self.n = other.n
        self.d = other.d
        self.f = other.f
        self.date = other.date
        self.idN = other.idN
        self.screenName = other.screenName
        self.first = other.first

class DB(userVertex):

    f_userprofile = open("user.txt", 'r')
    f_friendship = open("friend.txt", 'r')
    f_wordtweet = open("word.txt", 'r')

    userprofile = f_userprofile.readlines()
    friendship = f_friendship.readlines()
    wordtweet = f_wordtweet.readlines()

    idN = []
    date = []
    screenName = []
    count = 0

    userVertexList = []


    for i in userprofile:
        if count == 0:
            idN.append(i[0:len(i)-1])
            count += 1
        elif count == 1:
            date.append(i[0:len(i)-1])
            count += 1
        elif count == 2:
            screenName.append(i[0:len(i)-1])
            count += 1
        elif count == 3:
            count = 0

    for i in range(0, len(idN)):
        a = userVertex()
        a.idN = idN[i]
        a.date = date[i]
        a.screenName = screenName[i]
        a.n = i
        userVertexList.append(a)
    """userVertexList를 idN 순으로 sort"""

    tmp = userVertexList[:]
    v_mergesort(tmp, userVertexList, 0, len(userVertexList))

    """save friendship------------------------------------------------"""
    for i in friendship:
        if i == '\n':
            friendship.remove(i)

    searchcount = 0
    follower_idN = None
    follower_index = -1

    star_index = -1
    totalfriendship =0

    for idN in friendship:
        if searchcount == 0:
            if follower_idN == None:
                follower_idN = idN[0:len(idN)-1]
                for index in range(0,len(userVertexList)):
                    if userVertexList[index].idN == follower_idN:
                        follower_index = index
            else:
                if follower_idN != idN[0:len(idN)-1]:
                    follower_idN = idN[0:len(idN)-1]
                    for index in range(0,len(userVertexList)):
                        if userVertexList[index].idN == follower_idN:
                            follower_index = index
                    star_index = -1

        elif searchcount == 1:
            if follower_idN != None:

                for index in range(0,len(userVertexList)):
                    if userVertexList[index].idN == idN[0:len(idN)-1]:
                        star_index = index

                userVertexList[star_index].add(userVertexList[follower_index])
                userVertexList[star_index].friendnum += 1
                totalfriendship +=1
        if searchcount == 0:
            searchcount = 1
        else:
            searchcount = 0
    "end save friendship--------------------------------------------------"

    "save tweets----------------------------------------------------------"
    searchcount = 0
    tweetidN = None
    writeridx = -1
    flag = 0
    tweetscount = 0
    for line in wordtweet:
        if searchcount == 0:
            if tweetidN == None:
                tweetidN = line[0:len(line)-1]
                for index in range(0, len(userVertexList)):
                    if userVertexList[index].idN == tweetidN:
                        writeridx = index
                        flag = 1
                        searchcount += 1
            else:
                tweetidN = line[0:len(line)-1]
                if tweetidN == userVertexList[writeridx].idN:
                    flag = 1
                else:
                    for index in range(0, len(userVertexList)):
                        if userVertexList[index].idN == tweetidN:
                            writeridx = index
                            flag = 1

                searchcount += 1
        elif searchcount == 1:
            searchcount += 1
        elif searchcount == 2:
            if flag == 1:
                userVertexList[writeridx].tweets.append(line[0:len(line)-1])
                userVertexList[writeridx].tweetnum += 1
                tweetscount += 1
                flag = 0
                searchcount += 1
        elif searchcount == 3:
            searchcount = 0



    def readDataFiles(self):
        print("Total users: ", len(self.userVertexList))
        print("Total friendship records: ", self.totalfriendship)
        print("Total tweets: ", self.tweetscount)

    def averagefriend(self):
        return self.totalfriendship/len(self.userVertexList)

    def minfriend(self):
        min = self.userVertexList[0].friendnum
        for user in self.userVertexList:
            if min > user.friendnum:
                min = user.friendnum
        return min

    def maxfriend(self):
        max = self.userVertexList[0].friendnum
        for user in self.userVertexList:
            if max < user.friendnum:
                max = user.friendnum
        return max

    def averageTweets(self):
        return self.tweetscount/len(self.userVertexList)

    def minTweets(self):
        min = self.userVertexList[0].tweetnum
        for user in self.userVertexList:
            if min > user.tweetnum:
                min = user.tweetnum
        return min

    def maxTweets(self):
        max = self.userVertexList[0].tweetnum
        for user in self.userVertexList:
            if max < user.tweetnum:
                max = user.tweetnum
        return max
    def print_statistic(self):
        print("Average number of friends: ",self.averagefriend())
        print("Minimum friends: ",self.minfriend())
        print("Maximum number of friends: ",self.maxfriend())
        print("")
        print("Average tweets per user: ",self.averageTweets())
        print("Mininum tweets per user: ",self.minTweets())
        print("Maximum tweets per user: ",self.maxTweets())

    def mostWord(self):
        wordlist = []
        tweet = ""
        maxcount = 0
        tweetcount = 0
        maxtweet = []
        for user in self.userVertexList:
            wordlist += wordlist + user.tweets
        wordlist.sort()
        for i in range(0, len(wordlist)):
            if tweet == "":
                tweet = wordlist[i]
                tweetcount += 1
            else:
                if tweet == wordlist[i]:
                    tweetcount += 1
                elif tweet != wordlist[i] or i == len(wordlist)-1:
                    tweet = wordlist[i]
                    if maxcount <= tweetcount:
                        maxcount = tweetcount
                        maxtweet.append(wordlist[i-1])
                    tweetcount = 1
        return maxtweet

    def getUserVertexByTweet(self):
        targettweet = input("Enter the word: ")
        getuser = []
        for user in self.userVertexList:
            for tweet in user.tweets:
                if tweet == targettweet:
                    getuser.append(user)
                    break
        return getuser

    def user_Mosttweet(self):
        num_maxtweet = self.userVertexList[0].tweetnum
        maxtweetusers = []
        for user in self.userVertexList:
            if num_maxtweet < user.tweetnum:
                num_maxtweet = user.tweetnum
        for user in self.userVertexList:
            if user.tweetnum == num_maxtweet:
                maxtweetusers.append(user)
        more = maxtweetusers[0].tweetnum

        print("Top 1 : ", end ="")
        count = len(maxtweetusers)
        for i in range(0, count):
            print(maxtweetusers[i].screenName,"(",maxtweetusers[i].tweetnum,")", end=", ")
        print("")
        for i in range(0, 4):
            num_maxtweet = 0
            for user in self.userVertexList:
                if num_maxtweet < user.tweetnum and user.tweetnum < more:
                    num_maxtweet = user.tweetnum
            for user in self.userVertexList:
                if user.tweetnum == num_maxtweet:
                    maxtweetusers.append(user)
                    more = user.tweetnum
            print("Top",i+2,": ", end ="")
            for i in range(count,len(maxtweetusers)):
                print(maxtweetusers[i].screenName, "(",maxtweetusers[i].tweetnum,")", end=", ")
            print("")
            count = len(maxtweetusers)
        return maxtweetusers

    def removeMention(self):
        targettweet = input("Enter the word: ")
        for user in self.userVertexList:
            while 1:
                try:
                    user.tweets.remove(targettweet)
                except: break

    def removeUser(self):
        targettweet = input("Enter the word: ")
        removeduser = []
        for user in self.userVertexList:
            if targettweet in user.tweets:
                removeduser.append(user)
        for r_user in removeduser:
            self.userVertexList.remove(r_user)
        return removeduser




class Weight(Adj):
    def __init__(self, n, w):
        super().__init__(n)
        self.w = w

class DijkVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.d = INFTY
        self.priority = None
    def __repr__(self):
        return "(%a %a %a)" % (self.name,self.n,self.d)
    def add(self, v, w):
        a = Weight(v, w)
        a.next = self.first
        self.first = a
    def set_priority(self,n):
        self.priority = n
    def decrease_key(self, q):
        prio = self.priority
        ndx = prio.ndx
        q.decrease_key(ndx, self.d)

class Dijkstra:
    def __init__(self):
        self.vertices = []
        self.q = MinQueue()
    def add_vertex(self,name):
        n = len(self.vertices)
        v = DijkVertex(name)
        v.n = n
        self.vertices.append(v)
        return v
    def get_vertex(self,name):
        for v in self.vertices:
            if v.name == name:
                return v
        return None

    def print_vertex(self,n):
        print (self.vertices[n].name, end=' ')
        print (self.vertices[n].parent, end=' ')
        print (self.vertices[n].d, end=' ')
        p = self.vertices[n].first
        while p:
            print (p.n.name, end = ' ')
            print (p.w, end = ' ')
            p = p.next
        print('')

    def print_vertices(self):
        for i in range(len(self.vertices)):
            self.print_vertex(i)

    def relax(self, u):
        vset = self.vertices
        q = self.q
        p = u.first
        while p:
            v = p.n;
            d = u.d + p.w
            if d < v.d:
                v.d = d
                v.parent = u.n
                print(v)
                v.decrease_key(q)
            p = p.next

    def shortest_path(self):
        q = self.q
        vset = self.vertices
        for v in vset:
            n = PrioNode(v.d, v.n)
            v.set_priority(n)
            q.insert(n)
        while not q.is_empty():
            u = q.extract()
            self.relax(vset[u.n])
            WHITE = 0



class Queue:
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.sz = 0
        self.buf = []
    def create_queue(self,sz):
        self.sz = sz
        self.buf = list(range(sz))  # malloc(sizeof(int)*sz)
    def enqueue(self,val):
        self.buf[self.rear] = val
        self.rear = (self.rear + 1) % self.sz
    def dequeue(self):
        res = self.buf[self.front]
        self.front = (self.front + 1) % self.sz
        return res
    def is_empty(self):
        return self.front == self.rear

def print_vertex(vertices,n):
    print(vertices[n].screenName, end=' ')
    print(vertices[n].color, end=' ')
    print(vertices[n].parent, end=' ')
    print(vertices[n].d, end=':')
    p = vertices[n].first
    while p:
        print(vertices[p.n].screenName, end = ' ')
        p = p.next
    print('')

def g_transpose(vertices, vertices1):
    for i in range(len(vertices1)):
        vertices1[i].first = None
    for v in vertices:
        p = v.first
        while p:
            vertices1[p.n].add(v)
            p = p.next

class DepthFirstSearch:
    dfs_db = DB()
    def __init__(self):
        self.time = 0
        self.vertices = None

    def set_vertices(self, vertices):
        self.vertices = vertices
        for i in range(len(self.vertices)):
            self.vertices[i].n = i
    def dfs(self):
        for u in self.vertices:
            u.color = WHITE
            u.parent = -1
        self.time = 0
        for u in self.vertices:
            if u.color == WHITE:
                self.dfs_visit(u)
    def dfs_visit(self, u):
        self.time = self.time + 1
        u.d = self.time
        u.color = GRAY
        v = u.first
        while v:
            if self.vertices[v.n].color == WHITE:
                self.vertices[v.n].parent = u.n
                self.dfs_visit(self.vertices[v.n])
            v = v.next;
        u.color = BLACK
        self.time = self.time + 1
        u.f = self.time

    def print_scc(self, u):
        print(u.screenName, end=" ")
        vset = self.vertices
        if u.parent >= 0:
            self.print_scc(vset[u.parent])

    def scc_find(self, u):
        u.color = GRAY
        v = u.first
        found = False
        while v:
            if self.vertices[v.n].color == WHITE:
                found = True
                self.vertices[v.n].parent = u.n
                self.scc_find(self.vertices[v.n])
            v = v.next;
        if not found:
            print("SCC:", end=" ")
            self.print_scc(u)
            print ("")
        u.color = BLACK

    def print_vertex(self,n):
        print(self.vertices[n].screenName, end=' ')
        print(self.vertices[n].color, end=' ')
        print(self.vertices[n].parent, end=' ')
        print(self.vertices[n].d, end=' ')
        print(self.vertices[n].f, end=':')
        p = self.vertices[n].first
        while p:
            print(self.vertices[p.n].screenName, end = ' ')
            p = p.next
        print('')

    def print_vertices(self):
        for i in range(len(self.vertices)):
            self.print_vertex(i)
    def transpose(self):
        vertices1 = []
        for v in self.vertices:
            v1 = userVertex()
            v1.screenName = v.screenName
            v1.copy(v)
            vertices1.append(v1)
        g_transpose(self.vertices,vertices1)
        self.set_vertices(vertices1)

    def left(self,n):
        return 2*n+1

    def right(self,n):
        return 2*n+2

    def heapify(self,A,i,heapsize):
        vset = self.vertices
        l = self.left(i)
        r = self.right(i)
        if l < heapsize and vset[A[l]].f < vset[A[i]].f:
            largest = l
        else:
            largest = i
        if r < heapsize and vset[A[r]].f < vset[A[largest]].f:
            largest = r
        if largest != i:
            A[i],A[largest] = A[largest],A[i]
            self.heapify(A,largest,heapsize)

    def buildheap(self,A):
        for i in range(len(A)//2 + 1,0,-1):
            self.heapify(A,i-1,len(A))

    def heapsort(self,A):
        self.buildheap(A)
        for i in range(len(A),1,-1):
            A[i-1],A[0] = A[0],A[i-1]
            self.heapify(A,0,i - 1)

    def sort_by_f(self):
        vset = self.vertices
        sorted_indices = list(range(len(vset)))
        self.heapsort(sorted_indices)
        return sorted_indices

    def scc(self):
        self.dfs()
        self.print_vertices()
        self.transpose()
        sorted = self.sort_by_f()
        vset = self.vertices
        for v in vset:
            v.color = WHITE
            v.parent = -1
        for n in sorted:
            if self.vertices[n].color == WHITE:
                self.scc_find(vset[n])


class rbnode(object):

    def __init__(self, key):
        "Construct."
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        "String representation."
        return str(self.key)

    def __repr__(self):
        "String representation."
        return str(self.key)

class rbtree(object):
    def __init__(self, create_node=rbnode):
        self._nil = create_node(key=None)
        "Our nil node, used for all leaves."
        self._root = self.nil
        "The root of the tree."
        self._create_node = create_node
        "A callable that creates a node."

    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")

    def search(self, key, x=None):
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x


    def minimum(self, x=None):
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x


    def maximum(self, x=None):
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def insert_key(self, key):
        "Insert the key into the tree."
        self.insert_node(self._create_node(key=key))

    def insert_node(self, z):
        "Insert node z into the tree."
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        print("")
        self._insert_fixup(z)
        print("")
        print("")

    def _insert_fixup(self, z):
        "Restore red-black properties after insert."
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False


    def _left_rotate(self, x):
        "Left rotate x."
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        "Left rotate y."
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x


    def check_invariants(self):
        "@return: True iff satisfies all criteria to be red-black tree."

        def is_red_black_node(node):
            "@return: num_black"
            # check has _left and _right or neither
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            # check leaves are black
            if not node.left and not node.right and node.red:
                return 0, False

            # if node is red, check children are black
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            # descend tree and check black counts are balanced
            if node.left and node.right:

                # check children's parents are correct
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                # check children's counts are ok
                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red

def interface():
    print("""-----------------------------
0. Read data files
1. display statistics
2. Top 5 most tweeted words
3. Top 5 most tweeted users
4. Find users who tweeted a word (e.g., ’연세대’)
5. Find all people who are friends of the above users
6. Delete all mentions of a word
7. Delete all users who mentioned a word
8. Find strongly connected components
9. Find shortest path from a given user
99. Quit
Select Menu:""", end ="")

def main():
    db = DB()
    starvertex = []
    while 1:

        interface()
        menu = int(input())


        if menu == 0:
            db.readDataFiles()

        elif menu == 1:
            db.print_statistic()
        elif menu == 2:
            for word in db.mostWord():
                print(word,", ", end ="")

        elif menu == 3:
            starvertex = []
            for user in db.user_Mosttweet():
                starvertex.append(user)

        elif menu == 4:
            starvertex = []
            for user in db.getUserVertexByTweet():
                starvertex.append(user)
                print(user.screenName, end = ", ")
            if starvertex:
                print("")
                pass
            else:
                print("None")


        elif menu == 5:
            if starvertex:
                pass
            else:
                print("None")
            for vertex in starvertex:
                print(vertex.screenName, "'s friends: ", end = "")
                p = vertex.first
                if p == None:
                    print("None")
                else:
                    while p:
                        print(p.screenName,end = ', ')
                        p = p.next
                    print("")
        elif menu == 6:
            db.removeMention()

        elif menu == 7:
            for i in db.removeUser():
                print(i.screenName,end = ', ')
        elif menu == 8:
            print("구현되지 않은 기능입니다")
        elif menu == 9:
            print("구현되지 않은 기능입니다")
        elif menu == 99:
            print("수고하셨습니다")
            return
main()
