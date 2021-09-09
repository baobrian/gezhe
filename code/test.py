# #coding=utf-8
# import heapq
#
# def findMedian(array):
#     length = len(array)
#     minHeap = array[0:length // 2 + 1]
#     heapq.heapify(minHeap)
#     i = length // 2 + 1
#     while i < length:
#         heapq.heappushpop(minHeap, array[i])
#         i += 1
#     if length % 2:
#         return minHeap[0]
#     else:
#         return (heapq.heappop(minHeap) + minHeap[0]) / 2
#
# if __name__ == '__main__':
#
#     array1 = [2, 1,2,9,3, 3]
#     print(findMedian(array1) )
#     array2 = [1,6, 3, 4, 2, 9,10]
#     print(findMedian(array2))




class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None



class MaximumBinTree:
    def constructMaximumBinaryTree(self, nums) -> TreeNode:
        # 特判
        if not nums:
            return None
        # 找到数组中的最大值和对应的索引
        maxVal = max(nums)
        maxIndex = nums.index(maxVal)

        root = TreeNode(nums[maxIndex])
        # 递归构造左右子树
        root.left = self.constructMaximumBinaryTree(nums[:maxIndex])
        root.right = self.constructMaximumBinaryTree(nums[maxIndex + 1:])

        return root


if __name__ == '__main__':
    mbt=MaximumBinTree()
    ss=mbt.constructMaximumBinaryTree(nums=[3,2,1,6,0,5])

